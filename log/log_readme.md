**How to use logger:**

1. import the module: `from log.log_config import log, configlogging`
2. create a logger: `logger = configlogging()`
3. put a decorator on an each method you want to log (called, exeption): `@log(logger)`
4. use a logger to log additional events `logger.info('scan started on IP', self.ip)`

Logger levels:

* `logger.debug('debug message')`
* `logger.info('info message')`
* `logger.warn('warn message')`
* `logger.error('error message')`
* `logger.critical('critical message')`

**All parameters must be str!**