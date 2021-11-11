import "quill/dist/quill.snow.css";
import Quill, { QuillOptionsStatic } from "quill";

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