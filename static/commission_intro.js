async function get_dat() {
    let a_tag = document.getElementById("is_login")
    let pfp = document.getElementById("pfp")
    let drop_down_visibility = document.getElementById("dropdown")
    let dat = await fetch("/usr_inf", {
        method : "POST"
    })
    let response = await dat.json()
    if (response.verified) {
        //INIT PART
        a_tag.innerHTML = response.name
        pfp.src = response.image
        pfp.style.visibility = "visible"
    }
    else {
        drop_down_visibility.style.display = "none"
        return
    } 
}

get_dat()

async function logout() {
    let response = await fetch("/logout", {
        method : "POST"
    })
    let get_json = await response.json()
    if (get_json.status == "ok") {
        window.location.href = "/"
    }
}

function login() {
    window.location.href = "/login_google"
}