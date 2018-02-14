const path = require('path');
const CopyWebpackPlugin = require('copy-webpack-plugin');

const buildRoot = path.resolve(__dirname, "./js");
const outputRoot = path.resolve(__dirname, "./js/monaco");
const monacoEditorPath = './node_modules/monaco-editor-core/dev/vs';

module.exports = {
    watch: true,
    entry: path.resolve(buildRoot, "tab-code.js"),
    output: {
        filename: 'bundle.js',
        path: outputRoot
    },
    module: {
        noParse: /vscode-languageserver-types/
    },
    resolve: {
        extensions: ['.js'],
        alias: {
            'vs': path.resolve(buildRoot, monacoEditorPath)
        }
    },
    devtool: 'source-map',
    target: 'web',
    node: {
        fs: 'empty',
        child_process: 'empty',
        net: 'empty',
        crypto: 'empty'
    },
    plugins: [
        new CopyWebpackPlugin([
            {
                from: monacoEditorPath,
                to: 'vs'
            }
        ])
    ]
};