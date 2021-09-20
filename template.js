let node{index} = document.querySelector('#{node}');
node{index}.addEventListener('{eventName}',(e)=>{{
    console.log(e,document,window)
    customFunction(e,`{relation}`,`{index}`,`{nodeKeyName}`)
}})


