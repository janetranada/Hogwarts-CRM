function createSelection(name, options, targetContainer) {
    let selection = document.createElement("select");
    selection.setAttribute("name", name);
    for (let i = 0; i < options.length; i++) {
        let option = document.createElement("option");
        option.setAttribute('value', options[i]);
        option.innerText = options[i];
        selection.appendChild(option); 
    }
    targetContainer.appendChild(selection);
}

const desiredMagicContainer = document.getElementById('desired-magic')
const currentMagicContainer = document.getElementById('current-magic')
const magic = ['Alchemy', 'Animation', 'Conjuror', 'Disintegration', 'Elemental',
    'Healing', 'Illusion', 'Immortality', 'Invisibility', 'Invulnerability', 
    'Necromancer', 'Omnipresent', 'Omniscient', 'Poison', 'Possession', 'Self-detonation', 
    'Summoning', 'Water breathing']
const courses = ['Alchemy basics', 'Alchemy advanced', 'Magic for day-to-day life', 'Magic for medical professionals', 'Dating with magic']

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


fetch()