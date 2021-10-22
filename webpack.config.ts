import * as path from "path";
import * as webpack from "webpack";

const config: webpack.Configuration = {
    entry: {
        bootstrap: __dirname + "/prego-fe/js/bootstrap.js"
    },
    output: {
        path: path.resolve("./static/"),
        filename: "[name].js"
    },
    module: {
        rules: [
            {
                test: /\.css$/,
                use: [
                    "style-loader",
                    "css-loader"
                ]
            }
        ]
    }
}

export default config;