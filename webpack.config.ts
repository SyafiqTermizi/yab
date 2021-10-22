import * as path from "path";
import * as webpack from "webpack";

const config: webpack.Configuration = {
    entry: {
        script: __dirname + "/prego-fe/js/index.js",
    },
    output: {
        path: path.resolve("./static/"),
        filename: "[name]"
    },
    module: {
        rules: [
            {
                test: /\.scss$/,
                exclude: /node_modules/,
                use: [
                    {
                        loader: "file-loader",
                        options: { outputPath: "css/", name: "[name].min.css" }
                    },
                    "sass-loader"
                ]
            }
        ]
    }
}

export default config;