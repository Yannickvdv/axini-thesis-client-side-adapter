

var socket = new WebSocket("ws://localhost:8765");
var pageHasInitialized = false;

function sendWebsocketMessage(message) {
    // Send the JSON data to the server or handle it as needed
    if (socket.readyState === WebSocket.OPEN) {
        socket.send(message);
        console.log("Sent mutation data:", message);
    } else {
        console.warn("WebSocket not open, unable to send data.");
    }
}

function firstPageReload(){
    var changes = {};
    changes.label = "page_loaded";
    changes.title = document.title;
    changes.url = window.location.href;
    var jsonChanges = JSON.stringify(changes); 
    sendWebsocketMessage(jsonChanges);
}

function routeChange(event) {
    console.log(event)
}

function pageChanges(mutationsList){
    var changes = {
        label: "page_updated",
        characterData: [],
        attributes: [],
        childList: []
    };

    mutationsList.forEach(function (mutation) {  
        if (mutation.type === "characterData") {
            var mutationInfo = {
                type: "characterData",
                oldTextContent: mutation.oldValue,
                newTextContent: mutation.target.textContent,
                target: {
                    nodeId: String(mutation.target.id),
                    nodeName: mutation.target.nodeName,
                    nodeType: mutation.target.nodeType
                },
            }

            attrName = mutation.attributeName;
            mutationInfo.target[attrName] = mutation.target[attrName]
            changes.characterData.push(mutationInfo)
        }
        else if (mutation.type === "attributes") {
            var mutationInfo = {
                type: "attributes",
                attributeName: mutation.attributeName,
                oldAttributeValue: String(mutation.oldValue),
                newAttributeValue: String(mutation.target[mutation.attributeName]),
                target: {
                    nodeId: String(mutation.target.id),
                    nodeName: mutation.target.nodeName,
                    nodeType: mutation.target.nodeType,
                },
            }
            changes.attributes.push(mutationInfo)
        }
        else if (mutation.type === "childList") {
            var mutationInfo = {
                type: "childList",
                target: {
                    nodeId: String(mutation.target.id),
                    nodeName: mutation.target.nodeName,
                    nodeType: mutation.target.nodeType,
                },
                addedNodes: [],
                removedNodes: [],
            };

            mutation.addedNodes.forEach(function (node) {
                // Extract relevant information from added nodes
                var nodeData = {
                    type: node.nodeType,
                    nodeName: node.nodeName,
                    textContent: node.textContent,
                };
                mutationInfo.addedNodes.push(nodeData);
            });

            mutation.removedNodes.forEach(function (node) {
                // Extract relevant information from removed nodes
                var nodeData = {
                    nodeType: node.nodeType,
                    nodeName: node.nodeName,
                    textContent: node.textContent,
                };
                mutationInfo.removedNodes.push(nodeData);
            });

            changes.childList.push(mutationInfo);
        }
    });

    // Convert the extracted data to JSON
    var jsonChanges = JSON.stringify(changes);
    sendWebsocketMessage(jsonChanges)
}

// Create a WebSocket connection to the Python server
function mutationCallback(mutationsList, observer) {
    if (!pageHasInitialized) {
        firstPageReload();
        pageHasInitialized = true;
        return;
    }

    pageChanges(mutationsList);
}

// Use requestAnimationFrame to ensure the DOM is ready
requestAnimationFrame(function() {

    // Wait for the DOMContentLoaded event before running your code
    document.addEventListener('DOMContentLoaded', function() {
        // Create a MutationObserver and start observing the DOM
        var observer = new MutationObserver(mutationCallback);

        observer.observe(document.documentElement, { attributes: true, childList: true, characterData: true, subtree: true, attributeOldValue: true, characterDataOldValue: true});
    });
    
});

