function form(id, config = {
    target: null
}) {
    const element = document.getElementById(id);
    if (!config.target) {
        console.error("Form block #" + id + ": no target specified");
        return;
    }

    // find the form element in the block
    const form = element;
    form.setAttribute("onsubmit", "return false;");

    const method = form.getAttribute("method") || "POST";

    /*
    The form block supports:

    textarea
    select
    input elements with radio or checkbox type are given special consideration
    input elements for any other type usually works
    input elements with password type: note that the password is sent as plain text!
    */

    // set up submit handler
    form.addEventListener("submit", function(event) {
        // prevent the default action
        event.preventDefault();

        // build the payload
        var payload = {};

        // handle simple fields
        form.querySelectorAll("textarea[name], select[name]").forEach(function(field) {
            payload[field.name] = field.value;
        });

        // handle the more complex fields
        form.querySelectorAll("input[name]").forEach(function(field) {
            switch(field.type) {
                // radio buttons usually have a single selected option per name
                case 'radio':
                    if(field.checked) {
                        payload[field.name] = field.value;
                    }
                    break;

                // checkboxes are akin to a bitfield
                case 'checkbox':
                    // build a map of checked values for this name
                    if(typeof payload[field.name] === 'undefined') {
                        payload[field.name] = [];
                    }
                    if(field.checked) {
                        payload[field.name].push(field.value);
                    }
                    break;

                // default to storing the value
                default:
                    payload[field.name] = field.value;
                    break;
            }
        });

        // send the payload
        fetch(config.target, {
            method: method,
            body: JSON.stringify(payload),
            headers: {
                "Content-Type": "application/json",
            }
        })

    });


    // this is the only function that does not need a return statement
    // it is a single setup-only function
}