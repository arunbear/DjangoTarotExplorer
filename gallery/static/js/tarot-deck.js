class TarotDeck {
    constructor(allImages = [], backOfCardImgSrc = '') {
        this.allImages = allImages;
        this.pipImages = allImages.slice(0, 56);
        this.images = this.pipImages;
        this.backOfCardImgSrc = backOfCardImgSrc;
        this.cardsFromIndex = 0;
        this.numOfCards = 2;
        this.shuffleCards(this.images);
    }

    // Randomize array in-place using Durstenfeld shuffle algorithm
    shuffleArray(array) {
        for (let i = array.length - 1; i >= 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            const temp = array[i];
            array[i] = array[j];
            array[j] = temp;
        }
    }

    shuffleCards(images) {
        this.shuffleArray(images);
    }

    moreCardsToDeal() {
        return this.cardsFromIndex + this.numOfCards < this.images.length;
    }

    deal() {
        if (this.moreCardsToDeal()) {
            this.cardsFromIndex += this.numOfCards;
        }
        return this.getButtonStates();
    }

    back() {
        this.cardsFromIndex = (this.cardsFromIndex - this.numOfCards) % this.images.length;
        if (this.cardsFromIndex < 0) {
            this.cardsFromIndex = 0;
        }
        return this.getButtonStates();
    }

    resetDeck() {
        this.shuffleCards(this.images);
        this.cardsFromIndex = 0;
        return this.getButtonStates();
    }

    setIncludeTrumps(includeTrumps) {
        if (includeTrumps) {
            this.images = this.allImages;
        } else {
            this.images = this.pipImages;
        }
        this.resetDeck();
    }

    setNumOfCards(num) {
        this.numOfCards = num;
        this.cardsFromIndex = 0;
    }

    getButtonStates() {
        return {
            dealEnabled: this.moreCardsToDeal(),
            backEnabled: this.cardsFromIndex >= this.numOfCards,
            shuffleEnabled: this.cardsFromIndex >= this.numOfCards
        };
    }

    getCurrentCards() {
        const cards = [];
        for (let i = 0; i < this.numOfCards; i++) {
            const index = this.cardsFromIndex + i;
            if (index < this.images.length) {
                cards.push({
                    src: this.images[index],
                    caption: index + 1
                });
            } else if (i === 2 && this.numOfCards === 3 && this.images.length % 3 !== 0) {
                // Special case for 3 cards when deck doesn't divide evenly
                cards.push({
                    src: this.backOfCardImgSrc,
                    caption: ''
                });
            }
        }
        return cards;
    }
}

// Export for Node.js testing and browser use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TarotDeck;
} else if (typeof window !== 'undefined') {
    window.TarotDeck = TarotDeck;
}
