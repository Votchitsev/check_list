class Diagram {
    constructor(elementList) {
        this.elementList = elementList;
				this.initElementStyle();
    }

		initElementStyle() {
			for (let i = 0; i < this.elementList.length; i++) {
				this.setWidth(this.elementList.item(i));
				this.setColor(this.elementList.item(i));
			}
		}

    setWidth(element) {
    	const value = element.getAttribute('score');
    	element.style.width = `${value}%`;
    }

		setColor(element) {
			const value = element.getAttribute('score');

			if (value < 80) {
				element.style.backgroundColor = "rgb(253 110 110)";
			} 

			if (value >= 80 && value < 95) {
				element.style.backgroundColor = "#227022";
			}

			if (value > 95) {
				element.style.backgroundColor = "#a7a71d";
			}
		}
}

new Diagram(document.querySelectorAll('.diagram__item'));
