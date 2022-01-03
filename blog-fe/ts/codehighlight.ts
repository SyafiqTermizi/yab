import hljs from "highlight.js";
import "highlight.js/styles/github-dark.css"

hljs.configure({ languages: ["python", "javascript"] })

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("pre.ql-syntax").forEach((el: HTMLElement) => {
        hljs.highlightElement(el)
    })
})