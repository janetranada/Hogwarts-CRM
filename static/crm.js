function fetch_crm_data() {
    fetch("/get_data")
        .then(
            function (response) {
                if (response.status !== 200) {
                    console.log('Looks like there was a problem. Status Code: ' + response.status);                
                    return;
                }
                response.json().then(function (data) {
                    console.log('success', data);
                    create_charts(data)
                })
            })
}


function create_charts(_data){
    magic_list = _data['magic_name']
    current_magic_counter = _data["current_magic_counter"]
    desired_magic_counter = _data["desired_magic_counter"]
    curr_text = 'Current magic skills of Hogwarts students according to topic (since inception)'
    desired_text = 'Desired magic skills of Hogwarts students according to topic (since inception)'
    create_doughnut_Chart(magic_list, current_magic_counter, "Current Magic Skills", "currentMagicChart", curr_text);
    create_doughnut_Chart(magic_list, desired_magic_counter, "Desired Magic Skills", "desiredMagicChart", desired_text);
}


function create_doughnut_Chart(_label, _data, _datasetLabel, _targetContainer, _text) {    
    let ctx = document.getElementById(_targetContainer);
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: _label,
            datasets: [
                {
                    data: _data,
                    label: _datasetLabel,
                    backgroundColor: ['#f0134d', '#0c9463', '#f1fa3c', '#35495e',
                        '#deff8b', '#ee8572', '#8cba51', '#655c56',
                        '#ffcc00', '#c9485b', '#12cad6', '#697c37',
                        '#eb8242', '#ff8ba7', '#c2b0c9', '#ff7315',
                        '#f1d6ab', '#537ec5']
                },
            ]
        },
        options: {
            title: {
                display: true,
                text: _text
            },
            legend: {
                display: true,
                position: 'right'
            }
        }
    });
}

function createSelection(name, options, targetContainer) {
    let select_container = document.createElement("div")
    let selection = document.createElement("select");
    selection.setAttribute("name", name);
    for (let i = 0; i < options.length; i++) {
        let option = document.createElement("option");
        option.setAttribute('value', options[i]);
        option.innerText = options[i];
        selection.appendChild(option);
    }
    select_container.appendChild(selection)
    targetContainer.appendChild(select_container);
}

const desiredMagicContainer = document.getElementById('desired-magic')
const currentMagicContainer = document.getElementById('current-magic')
const magic = ['Alchemy', 'Animation', 'Conjuror', 'Disintegration', 'Elemental',
    'Healing', 'Illusion', 'Immortality', 'Invisibility', 'Invulnerability',
    'Necromancer', 'Omnipresent', 'Omniscient', 'Poison', 'Possession', 'Self-detonation',
    'Summoning', 'Water breathing']
const courses = ['Alchemy Basics',
    'Alchemy Advanced',
    'Magic for Day-to-Day Life',
    'Magic for Medical Professionals',
    'Dating with Magic']

document.getElementById('desired-magic-btn').addEventListener('click', () => {
    console.log('desired magic')
    select_name = "desired-magic"
    createSelection(select_name, magic, desiredMagicContainer)
})

document.getElementById('current-magic-btn').addEventListener('click', () => {
    console.log('current magic')
    select_name = "current-magic"
    createSelection(select_name, magic, desiredMagicContainer)
})

