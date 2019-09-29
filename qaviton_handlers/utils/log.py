import logging

FORMAT = '%(asctime)s [%(levelname)s] %(message)s'
LEVEL = logging.DEBUG
formatter = logging.Formatter(FORMAT)
log = logging.getLogger('qaviton-error-log')
log.setLevel(LEVEL)
handler = logging.StreamHandler()
handler.setLevel(LEVEL)
handler.setFormatter(formatter)
log.addHandler(handler)
