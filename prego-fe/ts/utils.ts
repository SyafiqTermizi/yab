export const getCSRFCookie = () => {
    const cookieKey = "csrftoken=";
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";").map(cookie => cookie.trim());
        const csrfCookie = cookies.filter(cookie => cookie.startsWith(cookieKey))[0]
        return csrfCookie.split(cookieKey)[1].trim()
    }
}