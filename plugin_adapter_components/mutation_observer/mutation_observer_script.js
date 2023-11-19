

var socket = new WebSocket("ws://localhost:8765");
var pageHasInitialized = false;

function sendWebsocketMessage(message) {
    return new Promise((resolve, reject) => {
        if (socket.readyState === WebSocket.OPEN) {
            socket.send(message);
            console.log("Sent mutation data:", message);
            resolve(); // Message sent successfully
        } else if (socket.readyState === WebSocket.CONNECTING) {
            // WebSocket is still connecting, wait for it to open
            socket.addEventListener('open', () => {
                socket.send(message);
                console.log("Sent mutation data:", message);
                resolve(); // Message sent successfully
            });
        } else {
            console.warn("WebSocket not open, unable to send data.");
            reject("WebSocket not open");
        }
    });
}

// function sendWebsocketMessage(message) {
//     // Send the JSON data to the server or handle it as needed
//     if (socket.readyState === WebSocket.OPEN) {
//         socket.send(message);
//         console.log("Sent mutation data:", message);
//     } else {
//         console.warn("WebSocket not open, unable to send data.");
//         socket.send(message);
//     }
// }

function pageChanges(mutationsList){
    var changes = {
        label: "page_updated",
        characterData: [],
        attributes: [],
        childList: []
    };

    mutationsList.forEach(function (mutation) {  
        var mutationInfo = {
            target: {
                nodeId: mutation.target.id ? String(mutation.target.id) : null,
                nodeName: mutation.target.nodeName ? mutation.target.nodeName : null,
                nodeType: mutation.target.nodeType
            },
        }

        if (mutation.type === "characterData") {
            mutationInfo.oldTextContent = (mutation.oldValue !== undefined) ? String(mutation.oldValue) : null
            mutationInfo.newTextContent = (mutation.target.textContent !== undefined)  ? String(mutation.target.textContent) : null

            changes.characterData.push(mutationInfo)
        }
        else if (mutation.type === "attributes") {
            attrName = mutation.attributeName;

            mutationInfo.attributeName = mutation.attributeName
            mutationInfo.oldAttributeValue = (mutation.oldValue !== undefined) ? String(mutation.oldValue) : null
            mutationInfo.newAttributeValue = (mutation.target[attrName] !== undefined) ? String(mutation.target[attrName]) : null
            
            changes.attributes.push(mutationInfo)
        }
        else if (mutation.type === "childList") {
            mutationInfo.addedNodes = [];
            mutationInfo.removedNodes = [];

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
    .then(() => {
        console.log("Message sent");
    })
    .catch(error => {
        console.error("Failed to send message:", error);
    });

}

// Create a WebSocket connection to the Python server
function mutationCallback(mutationsList, observer) {
    // if (!pageHasInitialized) {
    //     firstPageReload();
    //     pageHasInitialized = true;
    //     return;
    // }

    pageChanges(mutationsList);
}

// Use requestAnimationFrame to ensure the DOM is ready
// requestAnimationFrame(function() {
    // Wait for the DOMContentLoaded event before running your code
    document.addEventListener('DOMContentLoaded', function() {
        // Create a MutationObserver and start observing the DOM
        var observer = new MutationObserver(mutationCallback);

        observer.observe(document.documentElement, { attributes: true, childList: true, characterData: true, subtree: true, attributeOldValue: true, characterDataOldValue: true});
    }); 
// });

