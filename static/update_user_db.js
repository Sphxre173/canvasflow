async function request_update(uid, status) {
    let data = await fetch("/update_status", {
        method : "POST",
        headers : {
            "Content-Type" : "application/json"
        },
        body : JSON.stringify({
            "uid" : uid,
            "status" : status
        })
    })
    location.reload()
}