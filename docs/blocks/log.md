# Log Block
## Description
This block is used to log messages to a log display. It is useful for debugging purposes.

## Requirements
This block requires the following libraries:
- log.js

```html
<script src="/static/lib/log.js"></script>
```

## Preview
![preview](../img/log.png)

## Configuration
The log block has no configuration options.

## Actions
The log block takes in any string as input and logs it to the log display.

## Example
```html
<div id="log"></div>

<script>
    var log = log_block('log');
    connect_block(log, 'log');
</script>
