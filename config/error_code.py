def errors(error_code):
    error_dict = {
        0: ('OP_ERR_NONE', '정상 처리'),
        -10: ('OP_ERR_FAIL', '실패'),
        -101: ('OP_ERR_CONNECT', '서버 접속 실패'),
        -102: ('OP_ERR_VERSION', '버전 처리 실패')
    }

    result = error_dict[error_code]

    return result