def error_msg(error: str | None) -> str:
    if error:
        return f'''
Извините, что то пошло не так.
Ошибка: {error}
        '''
    return 'Извините, что то пошло не так.'
