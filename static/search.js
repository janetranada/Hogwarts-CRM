function fetch_data_and_search(_firstName, _lastName) {
    fetch("/get_data")
        .then(
            function (response) {
                if (response.status !== 200) {
                    return;
                }
                response.json().then(function (data) {
                    find_match(data, _firstName, _lastName);
                })
            })
}

function find_match(_data, _firstName, _lastName) {
    const result_container = document.getElementById('search-results');
    const search_fn_lower = _firstName.toLowerCase();
    const search_ln_lower = _lastName.toLowerCase();
    let total_hits = 0

    for (const key in _data.students) {
        let firstName = _data.students[key]['first_name'];
        let lastName = _data.students[key]['last_name'];
        let fn_lower = firstName.toLowerCase();
        let ln_lower = lastName.toLowerCase();
        let fn_capitalized = firstName.charAt(0).toUpperCase() + firstName.slice(1);
        let ln_capitalized = lastName.charAt(0).toUpperCase() + lastName.slice(1);

        if (_firstName == "" && _lastName == "") {
            render_message(result_container, "PLEASE PROVIDE SEARCH KEYS")
            return;
        } else if (fn_lower.includes(search_fn_lower) && ln_lower.includes(search_ln_lower)) {
            total_hits += 1;
            render_record(key, result_container, fn_capitalized, ln_capitalized);
        }
    }

    if (total_hits) {
        render_message(result_container, "*** END OF SEARCH RESULTS ***")
    } else {
        render_message(result_container, "*** NO RECORD FOUND ***")
    }
}

function render_record(_key, _mainContainer, _firstName, _lastName) {
    var name_container = "name_container" + _key
    var name_container = document.createElement("div")
    name_container.classList.add("search-result-item")
    name_container.innerHTML = `<a href="/student/${_key}" target='_blank'>${_firstName + " " + _lastName}</a>`
    _mainContainer.appendChild(name_container)
}

function render_message(_mainContainer, _message) {
    let msg_container = document.createElement("div");
    msg_container.classList.add("search-result-item", "red")
    msg_container.innerHTML = _message
    _mainContainer.appendChild(msg_container)

}

function delete_results() {
    while (result_container.hasChildNodes()) {
        result_container.removeChild(result_container.firstChild);
    };
}

const result_container = document.getElementById('search-results')
const search_btn = document.getElementById('search-btn')

search_btn.addEventListener('click', () => {
    delete_results();
    const first_name_input = document.getElementById('first-name-input').value.trim()
    const last_name_input = document.getElementById('last-name-input').value.trim()
    fetch_data_and_search(first_name_input, last_name_input)
})