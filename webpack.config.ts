import * as path from "path";
import * as webpack from "webpack";

const config: webpack.Configuration = {
    entry: {
        bootstrap: __dirname + "/blog-fe/ts/bootstrap.ts",
        editor: __dirname + "/blog-fe/ts/editor.ts",
        codehighlight: __dirname + "/blog-fe/ts/codehighlight.ts"
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
                resolve: {
                    extensions: [".ts"]
                }
            },
        ]
    }
}

export default config;