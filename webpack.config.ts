import * as path from "path";
import * as webpack from "webpack";

const config: webpack.Configuration = {
    entry: {
        bootstrap: __dirname + "/prego-fe/ts/bootstrap.ts",
        editor: __dirname + "/prego-fe/ts/editor.ts"
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
            },
            {
                test: /\.tsx?$/,
                use: 'ts-loader',
                exclude: /node_modules/,
            },
        ]
    }
}

export default config;