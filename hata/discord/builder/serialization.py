__all__ = ()

from itertools import islice


def create_serializer(builder_type, serialization_configuration):
    """
    Creates a new builder serializer for the given type.
    
    Parameters
    ----------
    builder_type : ``BuilderMeta``
        Builder type.
    serialization_configuration : ``SerializationConfiguration``
        Configuration for serialization.
    
    Returns
    -------
    serializer : `FunctionType`
    """
    def serializer(positional_parameters, keyword_parameters):
        """
        Generates serializer by `create_serializer`.
        
        Parameters
        ----------
        positional_parameters : `tuple<object>`
            Positional parameters to serialize.
        keyword_parameters : `dict<str, object>`
            Keyword parameters to serialize.
        
        Returns
        -------
        data : `dict<str, object> | FormData`
        """
        nonlocal builder_type
        nonlocal serialization_configuration
        
        positional_parameters_length = len(positional_parameters)
        if not positional_parameters_length:
            builder = builder_type()
        
        else:
            builder = positional_parameters[0]
            if isinstance(builder, builder_type):
                if positional_parameters_length > 1:
                    builder._with_positional_parameters(islice(positional_parameters, 1, positional_parameters_length))
            
            else:
                builder = builder_type()
                builder._with_positional_parameters(positional_parameters)
        
        if keyword_parameters:
            builder._with_keyword_parameters(keyword_parameters)
        
        return builder.serialise(serialization_configuration)
    
    
    return serializer
