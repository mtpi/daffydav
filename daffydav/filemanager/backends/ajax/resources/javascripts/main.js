var current_location = '';
var open_folders = [];

function updateNavigator()
{
    new Ajax.Updater('navigator', '?action=navigator', {
        method: 'post',
        parameters: {open_folders: open_folders.toJSON()}
        });
}

function updateContents()
{
    new Ajax.Updater('contents', '?action=contents', {
        method: 'get',
        });
}

function updateLocation()
{
    current_location = window.location.href.replace(/^https?:\/\/[^\/]+(\/[^?]*).*$/, '$1');
    var title = 'DaffyDav FileManager - ' + current_location;
    $('title_header').innerHTML = title;
    document.title = title;
}

function onLoad()
{
    // show location with an animation
    updateLocation();
    
    // load navigator panel
    updateNavigator();
    
    // load contents panel
    updateContents();
}

function openCloseDir(directory)
{
    if (open_folders.indexOf(directory) == -1) {
        //open folder
        open_folders.push(directory);
    } else {
        //close folder
        open_folders = open_folders.without(directory)
    }
    updateNavigator();
}
