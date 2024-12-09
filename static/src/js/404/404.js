$(document).ready(function () {
    // Lista de mensajes aleatorios para mostrar
    const messages = [
        "¡Vaya! Parece que algo se ha perdido.",
        "Esta página se ha escapado de nuestro radar.",
        "Lo sentimos, esta página no existe en nuestro universo.",
        "Oops, ¡esto no estaba en el mapa!",
        "¿En qué página estás? ¡No la encontramos!"
    ];
    const citas = [
        "«Los hombres de más amplia mentalidad saben que no hay una distinción clara entre lo real y lo irreal; que todas las cosas parecen lo que parecen sólo en vistud de los delicados instrumentos psíquicos y mentales de cada individuo, merced a los cuales llegamos a conocerlos; pero el prosaico materialismo de la mayoría condena como locura los destellos de clarividencia que traspasan el velo común del claro empirismo»",
        "«La muerte es misericordiosa, ya que de ella no hay retorno; pero para aquel que regresa de las cámaras más profundas de la noche, extraviado y consciente, no vuelve a haber paz»",
        "«La emoción más antigua y más intensa de la humanidad es el miedo, y el más antiguo y más intenso de los miedos es el miedo a lo desconocido»",
        "«El hombre que conoce la verdad está más allá del bien y del mal. El hombre que conoce la verdad ha comprendido que la ilusión es la realidad única y que la sustancia es la gran impostora»",
        "«Es una lástima que la mayor parte de la humanidad tenga una visión mental tan limitada a la hora de sopesar con calma y con inteligencia aquellos fenómenos aislados, cistos y sentidos sólo por unas pocas personas psíquicamente sensibles, que acontecen más allá de la experiencia común»",
        "«Pero más maravilloso que la sabiduría de los ancianos y que la sabiduría de los libros es la sabiduría secreta del océano»",
        "«Siempre que las estrellas estuvieran en posición, podían saltar de un mundo a otro a través de los cielos; mas cuando las estrellas no eran propicias, Ellos no podían vivir. Pero aunque no puedieran vivir, tampoco morirían realmente»",
        "«La cosa más misericordiosa del mundo, creo, es la incapacidad de la mente humana para correlacionar todos sus contenidos... algún día el empalme del conocimiento disociado abrirá perspectivas tan aterradoras de la realidad, y de nuestra posición espantosa en la misma, que nos volveremos locos por la revelación o huiremos de la luz a la paz y seguridad de una nueva Edad Oscura»",
        "«La base de todo verdadero horror cósmico es la violación del orden de la naturaleza, y las violaciones más profundas son siempre las menos concretas y descriptibles»",
        "«Ph'nglui mglw'nafh Cthulhu R'lyeh wgah'nagl fhtagn»",
        "«El mundo es realmente cómico, pero la broma es sobre la humanidad»",
        "«El hombre es un animal esencialmente supersticioso y temeroso. Quiten los dioses y santos cristianos de la manada y, sin falta, vendrán a adorar... a otra cosa»",
        "«Toda la vida es solo un conjunto de imágenes en el cerebro, entre las cuales no hay diferencia entre los nacidos de cosas reales y los nacidos de sueños internos, y no hay motivo para valorar a los unos encima de los otros»",
        "«El conocimiento trae consigo la maldición del entendimiento»",
        "«La locura es una forma de despertar, la única forma de comprender la verdadera realidad»",
        "«Hay secretos en el universo que el hombre no está destinado a conocer»",
        "«La esperanza es una ilusión reconfortante, pero solo eso, una ilusión»",
        "«El verdadero horror no es la monstruosidad física, sino la monstruosidad de la mente»",
        "«El verdadero infierno no es el fuego y la condenación, sino el conocimiento de la insignificancia»",
        "«El ser humano es solo un error de la naturaleza, un capricho olvidado del cosmos»",
        "«A mi parecer, no hay nada más misericordioso en el mundo que la incapacidad del cerebro humano de correlacionar todos sus contenidos. Vivimos en una plácida isla de ignorancia en medio de mares negros e infinitos, pero no fue concebido que debiéramos llegar muy lejos»"
    ];

    // Seleccionar un mensaje aleatorio
    let randomMessage = messages[Math.floor(Math.random() * messages.length)];
    $('#random-message').text(randomMessage);

    randomMessage = citas[Math.floor(Math.random() * citas.length)];
    $('#cita').text(randomMessage);

    $('#back-button').click(function() {
        window.history.back();  // Volver a la URL anterior en el historial
    });
});