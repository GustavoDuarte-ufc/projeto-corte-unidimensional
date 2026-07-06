export function saveTokens(
    access,
    refresh
){

    localStorage.setItem(
        "access_token",
        access
    );

    localStorage.setItem(
        "refresh_token",
        refresh
    );
}

export function getAccessToken(){

    return localStorage.getItem(
        "access_token"
    );
}

export function getRefreshToken(){

    return localStorage.getItem(
        "refresh_token"
    );
}

export function removeTokens(){

    localStorage.removeItem(
        "access_token"
    );

    localStorage.removeItem(
        "refresh_token"
    );
}

export function setAccessToken(
    token
){
    localStorage.setItem(
        "access_token",
        token
    );
}