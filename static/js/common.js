function notify_this(message_text, message_type) {
    $.notify({
        message: message_text
    }, {
        // settings
        type: message_type,
        z_index: 100000,
        placement: {
            from: "bottom",
            align: "right"
        },
        animate: {
            enter: 'animated fadeInDown',
            exit: 'animated fadeOutUp'
        }
    });
}