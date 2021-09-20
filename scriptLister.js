let customFunction = new Function('e','relation','index','nodeKeyName',`
let customEvent = new CustomEvent('dispatchEventLister',{detail:{
    hazcheeseburger: relation,
    index:index,
    nodeKeyName:nodeKeyName,
    eventInfo : e
}})
document.dispatchEvent(customEvent)
`)
let node1 = document.querySelector('#node1');
node1.addEventListener('click',(e)=>{
    console.log(e,document,window)
    customFunction(e,`describe`,`1`,`1-1`)
})



let node2 = document.querySelector('#node2');
node2.addEventListener('click',(e)=>{
    console.log(e,document,window)
    customFunction(e,`{'nodeName': '2111', 'child': [{'nodeName': '2111-12'}, {'nodeName': '2111-14'}]}`,`2`,`2-1`)
})



let node4 = document.querySelector('#node3');
node4.addEventListener('click',(e)=>{
    console.log(e,document,window)
    customFunction(e,`describe`,`4`,`2-2`)
})



let node6 = document.querySelector('#node4');
node6.addEventListener('click',(e)=>{
    console.log(e,document,window)
    customFunction(e,`describe`,`6`,`2-3`)
})



let node20 = document.querySelector('#node12');
node20.addEventListener('click',(e)=>{
    console.log(e,document,window)
    customFunction(e,`{'nodeName': '2911', 'child': [{'nodeName': '2911-12'}, {'nodeName': '2911-14'}]}`,`20`,`29-1`)
})



