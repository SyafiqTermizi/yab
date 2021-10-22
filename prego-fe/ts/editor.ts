import "quill/dist/quill.snow.css";
import Quill, { QuillOptionsStatic } from "quill";

const options: QuillOptionsStatic = {
    theme: "snow",
    placeholder: "Insert text here..",
    modules: {
        toolbar: [
            [{ "header": [1, 2, 3, 4, 5, 6, false] }],

            ["bold", "italic", "underline", "strike"],
            ["blockquote", "code-block"],

            [{ "list": "ordered" }, { "list": "bullet" }],

            ["image"],
        ]
    },
};

new Quill("#editor", options)