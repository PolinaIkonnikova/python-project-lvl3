import traceback


MESSAGES = {'writing problem': 'Some problems with writing in files.',
            'invalid url': 'The invalid url, please check writing.',
            'connect error': 'Check up internet connection.',
            'request error': 'Something wrong with url. '
                             'Check up internet connection.',
            'no permissions': "Unfortunately you haven't permissions "
                              "for using this directory {}, "
                              "please choose another directory. ",
            'not found dir': "The directory not found or not "
                             "a directory, please try again!",
            'resource dir': "The directory for resources: {}",
            'no resources': "The page hasn't resources for downloading.",
            'dir exists': 'The directory for resources exists. '
                          'Perhaps the page has already been loaded!',
            'unexpected_err': 'Unexpected error! Try to change url or '
                              'output directory and '
                              'check up internet connection.',
            'success loading': 'The page {} has loaded!',
            '404': 'The page not found, sorry.',
            '3XX': 'Oh please.. come on. Just relax and take'
                   ' a glass of vine, kiss your partner or play '
                   'with your dog or do some really useful. '
                   'STOP AWAY FROM THE COMPUTER!',
            '4XX': 'There is a browser error, try again later!',
            '5XX': 'Something went wrong with server connection =('}


def traceback_message(excp):
    return '\n'.join(traceback.format_exc().splitlines()[:-2]) +\
           '\n  {} ({})'.format(excp, excp.__class__)


def user_friendly_message(mes_key, *args):
    if not args:
        if mes_key == '404':
            print(MESSAGES[mes_key])
        elif mes_key[0] == '3':
            print(MESSAGES['3XX'])
        elif mes_key[0] == '4':
            print(MESSAGES['4XX'])
        elif mes_key[0] == '5':
            print(MESSAGES['5XX'])
        else:
            print(MESSAGES[mes_key])
    else:
        arg = args[0]
        print(MESSAGES[mes_key].format(arg))
    return
