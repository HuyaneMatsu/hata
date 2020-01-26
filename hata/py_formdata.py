# -*- coding: utf-8 -*-
__all__ = ('Formdata', )

from io import IOBase
from urllib.parse import urlencode
from .dereaddons_local import multidict
from .py_hdrs import CONTENT_TYPE, CONTENT_TRANSFER_ENCODING, CONTENT_LENGTH
from .py_multipart import MultipartWriter,create_payload,BytesPayload
from json import dumps as dump_to_json

#Helper class for multipart/form-data and
#application/x-www-form-urlencoded body generation.

class Formdata(object):

    __slots__=('fields', 'is_multipart', 'quote_fields', 'writer', )

    def __init__(self,quote_fields=True):
        self.writer=MultipartWriter('form-data')
        self.fields=[]
        self.is_multipart=False
        self.quote_fields=quote_fields
    
    @classmethod
    def fromfields(cls,data):
        self=cls()
        if isinstance(data,dict):
            data=list(data.items())
        elif isinstance(data,(list,tuple)):
            data=list(data)
        else:
            data=[data]

        while data:
            field=data.pop(0)
            if isinstance(field,IOBase):
                self.add_field(getattr(field,'name','unknown'),field)
            elif isinstance(field,multidict):
                data.extend(field.items())
            elif isinstance(field,(tuple,list)) and len(field)==2:
                self.add_field(*field)
            else:
                raise TypeError(f'Formdata.fromfields got unhandleable type: {type(field)!r}')
                
        return self
        
    def add_field(self,name,value,content_type=None,filename=None,transfer_encoding=None):

        if isinstance(value,IOBase):
            self.is_multipart=True
        elif isinstance(value,(bytes,bytearray,memoryview)):
            if filename is None and transfer_encoding is None:
                filename=name

        type_options=multidict()
        type_options['name']=name

        if (filename is not None):
            if not isinstance(filename,str):
                raise TypeError(f'Filename must be an instance of str. Got: {filename!r}')
        if (filename is None) and isinstance(value,IOBase):
            filename=getattr(value,'name',name)
        if (filename is not None):
            type_options['filename']=filename
            self.is_multipart=True

        header={}
        if content_type is not None:
            if not isinstance(content_type, str):
                raise TypeError(f'Content_type must be an instance of str. Got: {content_type!r}')
            header[CONTENT_TYPE]=content_type
            self.is_multipart=True
        if transfer_encoding is not None:
            if not isinstance(transfer_encoding, str):
                raise TypeError(f'Transfer_encoding must be an instance of str. Got: {transfer_encoding!r}')
            header[CONTENT_TRANSFER_ENCODING] = transfer_encoding
            self.is_multipart=True

        self.fields.append((type_options,header,value))

    def _gen_form_urlencoded(self,encoding):
        # form data (x-www-form-urlencoded)
        data=[]
        for type_options,header,value in self.fields:
            data.append((type_options['name'],value))

        if encoding=='utf-8':
            content_type='application/x-www-form-urlencoded'
        else:
            content_type=f'application/x-www-form-urlencoded; charset={encoding}'

        return BytesPayload(urlencode(data,doseq=True,encoding=encoding).encode(),content_type=content_type)

    def _gen_form_data(self,encoding):
        #Encode a list of fields using the multipart/form-data MIME format
        for type_options,header,value in self.fields:
            try:
                if CONTENT_TYPE in header:
                    part=create_payload(value,content_type=header[CONTENT_TYPE],
                        header=header,encoding=encoding,**type_options.kwargs())
                else:
                    part=create_payload(value,header=header,encoding=encoding)
            
            except Exception as err:
                raise TypeError(f'Can not serialize value: type: {type(value)!r}, header: {header!r}, value: {value!r}') from err
            
            if type_options:
                part.set_content_disposition('form-data', type_options.kwargs(), quote_fields=self.quote_fields)
                part.headers.popall(CONTENT_LENGTH,None)
            
            self.writer.append_payload(part)
        
        return self.writer

    def __call__(self,encoding='utf-8'):
        if self.is_multipart:
            return self._gen_form_data(encoding)
        else:
            return self._gen_form_urlencoded(encoding)

    def add_json(self,data):
        if data:
            type_options=multidict()
            type_options['name']='data_json'
            data=dump_to_json(data,separators=(',',':'),ensure_ascii=True)
            self.fields.append((type_options,{},data))

    def __repr__(self):
        result=[f'<{self.__class__.__name__} [']
        for type_options,header,value in self.fields:
            value=repr(value)
            if len(value)>40:
                value=object.__repr__(value)
            result.append(f'({type_options}, {header}, {value}), ')
        result.append(']>')
        return ''.join(result)

    __str__=__repr__
