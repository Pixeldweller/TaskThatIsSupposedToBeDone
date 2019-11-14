let lastSelectedId = undefined;
let lastSelectedRow = undefined;
let secondTimeClicked = false;

function setSelectedRow(row, target_id) {
    if (lastSelectedRow !== undefined) {
        lastSelectedRow.classList.remove('selected');
    }
    row.classList.add('selected');
    if (lastSelectedRow === row) {
        lastSelectedRow.classList.remove('selected');
        lastSelectedRow = undefined;
        lastSelectedId = undefined;
        toggleSelectionButtons(false);
        secondTimeClicked = false;
    } else {
        lastSelectedId = target_id;
        lastSelectedRow = row;
        toggleSelectionButtons(true);
        secondTimeClicked = false;
    }
}

function checkDeselect(row,id) {
    if (lastSelectedRow === row) {
        if (secondTimeClicked) {
            lastSelectedRow.classList.remove('selected');
            lastSelectedRow = undefined;
            lastSelectedId = undefined;
            toggleSelectionButtons(false);
            secondTimeClicked = false;
        } else {
            secondTimeClicked = true;
        }

    } else {
        setSelectedRow(row,id);
    }
}

function toggleSelectionButtons(selectionAvailable) {
    var elements = document.getElementsByClassName('needsSelection');
    var i;
    for (i = 0; i < elements.length; i++) {
        elements[i].disabled = !selectionAvailable;
    }

    setTimeout(500);
    if (selectionAvailable) {
        elements = document.getElementsByClassName("fadeInObject");
        for (i = 0; i < elements.length; i++) {
            elements[i].classList.add('show');
        }
    } else {
        elements = document.getElementsByClassName("fadeInObject");
        for (i = 0; i < elements.length; i++) {
            elements[i].classList.remove('show');
        }
    }
}

function openDetailPage(objectType) {
    if (lastSelectedId === undefined) {
        alert('Sie haben kein Element ausgewählt.');
    } else {
        window.location = "/" + objectType + "/show/" + lastSelectedId;
    }
}

function openEditPage(objectType) {
    if (lastSelectedId === undefined) {
        alert('Sie haben kein Element ausgewählt.');
    } else {
        window.location = "/" + objectType + "/edit/" + lastSelectedId;
    }
}

function openDeletePage(objectType) {
    if (lastSelectedId === undefined) {
        alert('Sie haben kein Element ausgewählt.');
    } else {
        window.location = "/" + objectType + "/delete/" + lastSelectedId;
    }
}
