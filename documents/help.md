Module help
===========

Classes
-------

`Help()`
:   This class handles the Help functionality.
    
    Constructor to initialize command dictionary and payload object
    
    :param:
    :type:
    :raise:
    :return: None
    :rtype: None

    ### Class variables

    `command_help`
    :

    `commands_dictionary`
    :

    ### Methods

    `help(self, command_name)`
    :   Creates a payload blocks for particular command
        
        :param command_name: Command name
        :type command_name: str
        :raise:
        :return: Blocks list containing details of a particular command provided in parameter
        :rtype: list

    `help_all(self)`
    :   Creates a payload with the help details for all commands
        
        :param:
        :type:
        :raise:
        :return: Payload object containing helper details of all commands
        :rtype: dict[str, Any]