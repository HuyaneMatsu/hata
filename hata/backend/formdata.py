# -*- coding: utf-8 -*-
__all__ = ('Formdata', )

from io import IOBase
from urllib.parse import urlencode
from json import dumps as dump_to_json

from .dereaddons_local import multidict

from .hdrs import CONTENT_TYPE, CONTENT_TRANSFER_ENCODING, CONTENT_LENGTH
from .multipart import MultipartWriter, create_payload, BytesPayload


# Helper class for multipart/form-data and application/x-www-form-urlencoded body generation.

class Formdata(object):
    
    __slots__ = ('fields', 'is_multipart', 'quote_fields', )
    
    def __init__(self, quote_fields=True):
        self.fields = []
        self.is_multipart = False
        self.quote_fields = quote_fields
    
    @classmethod
    def fromfields(cls, data):
        self = cls()
        if isinstance(data, dict):
            data = list(data.items())
        elif isinstance(data, (list, tuple)):
            data = list(data)
        else:
            data = [data]
        
        while data:
            field = data.pop(0)
            fiend_type = field.__class__
            if issubclass(fiend_type, IOBase):
                self.add_field(getattr(field, 'name', 'unknown'), field)
            elif issubclass(fiend_type, multidict):
                data.extend(field.items())
            elif issubclass(fiend_type, (tuple, list)) and len(field) == 2:
                self.add_field(*field)
            else:
                raise TypeError(f'`Formdata.fromfields` got unhandleable type: {fiend_type.__name__}.')
                
        return self
        
    def add_field(self, name, value, content_type=None, filename=None, transfer_encoding=None):
        
        if isinstance(value, IOBase):
            self.is_multipart = True
        elif isinstance(value, (bytes, bytearray, memoryview)):
            if (filename is None) and (transfer_encoding is None):
                filename = name
        
        type_options = multidict()
        type_options['name'] = name
        
        if (filename is not None):
            if not isinstance(filename, str):
                raise TypeError(f'Filename must be an instance of `str`, got: {filename.__class__.__name__}.')
        
        if (filename is None) and isinstance(value, IOBase):
            filename = getattr(value, 'name', name)
        
        if (filename is not None):
            type_options['filename'] = filename
            self.is_multipart = True
        
        headers = {}
        if (content_type is not None):
            if not isinstance(content_type, str):
                raise TypeError(f'Content_type must be an instance of str. Got: {content_type!r}.')
            headers[CONTENT_TYPE] = content_type
            self.is_multipart = True
        
        if (transfer_encoding is not None):
            if not isinstance(transfer_encoding, str):
                raise TypeError(f'Transfer_encoding must be an instance of str. Got: {transfer_encoding!r}.')
            headers[CONTENT_TRANSFER_ENCODING] = transfer_encoding
            self.is_multipart = True
        
        self.fields.append((type_options, headers, value))
    
    def _gen_form_urlencoded(self, encoding):
        # form data (x-www-form-urlencoded)
        data = []
        for type_options, header, value in self.fields:
            data.append((type_options['name'], value))
        
        if encoding == 'utf-8':
            content_type = 'application/x-www-form-urlencoded'
        else:
            content_type = f'application/x-www-form-urlencoded; charset={encoding}'
        
        return BytesPayload(urlencode(data, doseq=True, encoding=encoding).encode(), {'content_type': content_type})
    
    def _gen_form_data(self, encoding):
        # Encode a list of fields using the multipart/form-data MIME format
        writer = MultipartWriter('form-data')
        for type_options, headers, value in self.fields:
            try:
                payload_kwargs = {
                    'headers': headers,
                    'encoding': encoding,
                        }
                
                try:
                    content_type = headers[CONTENT_TYPE]
                except KeyError:
                    pass
                else:
                    payload_kwargs['content_type'] = content_type
                    
                    if type_options:
                        payload_kwargs.update(type_options.kwargs())
                
                part = create_payload(value, payload_kwargs)
            
            except BaseException as err:
                raise TypeError(f'Can not serialize value: type: {value.__class__!r}, headers: {headers!r}, value: '
                    f'{value!r}.') from err
            
            if type_options:
                part.set_content_disposition('form-data', type_options.kwargs(), quote_fields=self.quote_fields)
                part.headers.popall(CONTENT_LENGTH, None)
            
            writer.append_payload(part)
        
        return writer
    
    def __call__(self, encoding='utf-8'):
        if self.is_multipart:
            return self._gen_form_data(encoding)
        else:
            return self._gen_form_urlencoded(encoding)
    
    def add_json(self, data):
        if data:
            type_options = multidict()
            type_options['name'] = 'data_json'
            data = dump_to_json(data, separators=(',', ':'), ensure_ascii=True)
            self.fields.append((type_options, {}, data))
    
    def __repr__(self):
        result = ['<', self.__class__.__name__, ' [']
        
        fields = self.fields
        limit = len(fields)
        if limit:
            index = 0
            while True:
                type_options, headers, value = fields[index]
                result.append('(')
                result.append(repr(type_options))
                result.append(', ')
                result.append(repr(headers))
                result.append(', ')
                result.append(repr(value))
                result.append(')')
                
                index += 1
                if index == limit:
                    break
                    
                result.append(', ')
                continue
        
        result.append(']>')
        return ''.join(result)
    
    __str__ = __repr__
