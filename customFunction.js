let customFunction = new Function('e','relation','index','nodeKeyName',`
let customEvent = new CustomEvent('dispatchEventLister',{detail:{
    hazcheeseburger: relation,
    index:index,
    nodeKeyName:nodeKeyName,
    eventInfo : e
}})
document.dispatchEvent(customEvent)
`)