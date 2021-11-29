import "quill/dist/quill.snow.css";
import Quill, { QuillOptionsStatic } from "quill";

export function getCookie(name: string) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const options: QuillOptionsStatic = {
    theme: "snow",
    placeholder: "Insert text here..",
    modules: {
        toolbar: [
            [{ "header": [1, 2, 3, 4, 5, 6, false] }],

            ["bold", "italic", "underline", "strike", "link"],
            ["blockquote", "code-block"],

            [{ "list": "ordered" }, { "list": "bullet" }],

            ["image"],
        ]
    },
};

const editor = new Quill("#editor", options);

// Set editor initial data if available
const data = JSON.parse(document.getElementById("initial_data").textContent);
if (data) {
    editor.setContents(JSON.parse(data), "user");
}

// Handle form submission
document.getElementById("post_form").onsubmit = () => {
    const editorData = editor.getContents();
    const jsonBodyTextArea = document.getElementById("json_body") as HTMLInputElement;
    jsonBodyTextArea.value = JSON.stringify(editorData);

    const editorHTMLData = document.getElementsByClassName("ql-editor")[0].innerHTML;
    const htmlBodyTextArea = document.getElementById("html_body") as HTMLInputElement;
    htmlBodyTextArea.value = editorHTMLData;
    return true;
}

function selectLocalImage() {
    const input = document.createElement("input");
    input.setAttribute("type", "file");
    input.click();

    // Listen upload local image and save to server
    input.onchange = () => {
        const file = input.files[0];

        // file type is only image.
        if (/^image\//.test(file.type)) {
            saveToServer(file);
        } else {
            console.warn("You could only upload images.");
        }
    };
}

function saveToServer(file: File) {
    const fd = new FormData();
    fd.append("image", file);

    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/en/posts/create/image/", true);
    xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhr.onload = () => {
        if (xhr.status === 200) {
            // this is callback data: url
            const url = JSON.parse(xhr.responseText).data;
            console.log(url)
            insertToEditor(url.image);
        }
    };
    xhr.send(fd);
}


function insertToEditor(url: string) {
    // push image url to rich editor.
    const range = editor.getSelection();
    editor.insertEmbed(range.index, "image", url);
}

// quill editor add image handler
editor.getModule("toolbar").addHandler("image", () => {
    selectLocalImage();
});
