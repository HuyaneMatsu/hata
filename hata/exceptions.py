# -*- coding: utf-8 -*-

##| Code  | Meaning               | Behaviour     |
##|-------|-----------------------|---------------|
##| 200   | OK                    | return        |
##| 201   | CREATED               | return        |
##| 204   | NO CONTENT            | return        |
##| 304   | NOT MODIFIED          | return        |
##| 400   | BAD REQUEST           | raise         |
##| 401   | UNAUTHORIZED          | raise         |
##| 403   | FORBIDDEN             | raise         |
##| 404   | NOT FOUND             | raise         |
##| 405   | METHOD NOT ALLOWED    | raise         |
##| 429   | TOO MANY REQUESTS     | ratelimited   |
##| 500   | SERVER ERRROR         | retry         |
##| 502   | GATEWAY UNAVAILABLE   | retry         |
##| 5XX   | SERVER ERROR          | raise         |

__all__ = ('DiscordException', )

class DiscordException(Exception):
    def __init__(self,response,data):
        Exception.__init__(self)
        self.response=response
        self.data=data
        self._messages=None
        self._code=None
        
    @property
    def messages(self):
        messages=self._messages
        if messages is None:
            return self._cr_messages()
        return messages

    def _cr_messages(self):
        messages=[]
        code=self.code
        message_parts=[]
        data=self.data
        if type(data) is dict:
            message_base= data.get('message','')
            error_datas = data.get('errors')
            if error_datas:
                stack=[[(None,error_datas,)]]
                while True:
                    line=stack[-1]
                    if not line:
                        del stack[-1]
                        if not stack:
                            break
                            
                        del stack[-1][-1]
                        if not message_parts:
                            continue
                            
                        del message_parts[-1]
                        if not message_parts:
                            continue
                        
                        if message_parts[-1]!='.':
                            continue
                        
                        del message_parts[-1]
                        continue
                    
                    key,value=line[-1]
                    
                    if type(value) is dict:
                        if (key is not None):
                            if key.isdigit():
                                # this should not be first ever
                                message_parts.append(f'[{key}]')
                            else:
                                if message_parts:
                                    message_parts.append('.')
                                message_parts.append(key)
                        try:
                            error_datas=value['_errors']
                        except KeyError:
                            stack.append(list(value.items()))
                            continue
                        
                        for error_data in error_datas:
                            error_code=error_data.pop('code','ERROR')
                            error_message=error_data.pop('message','')
                            if error_data:
                                error_extra=' '.join(f'{key}={value!r}' for key,value in error_data.items())
                                if error_message:
                                    error_message=f'{error_message!r} {error_extra}'
                                else:
                                    error_message=error_extra
                            elif error_message:
                                error_message=repr(error_message)
                            
                            if message_parts:
                                message_parts.append('.')
                            
                            message_parts.append(f'{error_code}({error_message})')
                            messages.append(''.join(message_parts))
                            del message_parts[-1]
                            if not message_parts:
                                continue
                            
                            if message_parts[-1]!='.':
                                continue
                            
                            del message_parts[-1]
                            continue
                        
                        del line[-1]
                        if not message_parts:
                            continue
                            
                        del message_parts[-1]
                        
                        if not message_parts:
                            continue
                            
                        if message_parts[-1]!='.':
                            continue
                        
                        del message_parts[-1]
                        continue
                    
                    if key.isdigit():
                        message_parts.append(f'[{key}]')
                    else:
                        message_parts.append('.')
                        message_parts.append(key)
                    message_parts.append('.')
                    message_parts.append(value)
                    messages.append(''.join(message_parts))
                    del line[-1]
                    del message_parts[-3:]
                    if not message_parts:
                        continue
                    
                    if message_parts[-1]!='.':
                        continue
                    
                    del message_parts[-1]
                    
        else:
            message_base=''

        message_parts.append(f'{self.__class__.__name__} {self.response.reason} ({self.response.status})')
        
        if code:
            message_parts.append(f', code=')
            message_parts.append(code.__repr__())

        if message_base:
            message_parts.append(': ')
            message_parts.append(message_base)
        elif messages:
            message_parts.append(':')
            
        messages.append(''.join(message_parts))
        messages.reverse()
                    
        self._messages=messages
        return messages
    
    def __repr__(self):
        return '\n'.join(self.messages)

    __str__=__repr__

    @property
    def code(self):
        code=self._code
        if code is None:
            return self._cr_code()
        return code

    def _cr_code(self):
        if type(self.data) is dict:
            code=self.data.get('code',0)
        else:
            code=0
        
        self._code=code
        return code

    @property
    def status(self):
        return self.response.status


