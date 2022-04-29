var o2s=(o)=>{ try{ return JSON.stringify(o) }catch(ex) {} }
var s2o=(s)=>{ try{ return JSON.parse(s) } catch(ex){} }
var json_api = (u,a,m,cb)=>{
    var _cb = s=>(cb||console.log)(s2o(s),s);
    var x = new XMLHttpRequest();
    x.onreadystatechange=()=>(x.readyState==4)?_cb(x.responseText):null;
    x.onerror=(e)=>_cb(e);
    x.open(m,u,true);
    x.setRequestHeader('Accept', 'application/json');
    //x.setRequestHeader('Content-Type', 'application/json');
    x.send(a);
    return x;
}
