var jsonata = require("jsonata");

exports.handler = async function(event, context) {
    var expression_string = event.jsonata_expression;
    var data = event.data;
    var expression = jsonata(expression_string);
    return expression.evaluate(event);
}