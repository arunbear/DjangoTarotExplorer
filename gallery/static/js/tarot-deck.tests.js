// Test data for TarotDeck tests - 56 pip cards + 22 trumps = 78 total tarot cards
const mockImages = [
    // Pips (56 cards: 14 each for cups, coins, swords, wands)
    ...Array.from({length: 14}, (_, i) => `cups-${i + 1}.jpg`),
    ...Array.from({length: 14}, (_, i) => `coins-${i + 1}.jpg`),
    ...Array.from({length: 14}, (_, i) => `swords-${i + 1}.jpg`),
    ...Array.from({length: 14}, (_, i) => `wands-${i + 1}.jpg`),
    // Trumps (22 cards)
    ...Array.from({length: 22}, (_, i) => `trump-${i}.jpg`)
];

// QUnit test suite for TarotDeck class
class TarotDeckTests {
    static registerQUnitTests() {
        QUnit.module('TarotDeck Initialization');

        QUnit.test('should initialize with correct values', assert => {
            const deck = new TarotDeck(mockImages, 'back.jpg');
            
            assert.deepEqual(deck.allImages, mockImages, 'allImages should match');
            assert.equal(deck.pipImages.length, 56, 'pipImages should have 56 cards');
            assert.equal(deck.cardsFromIndex, 0, 'cardsFromIndex should be 0');
            assert.equal(deck.numOfCardsToDeal, 2, 'numOfCards should be 2');
            assert.equal(deck.backOfCardImgSrc, 'back.jpg', 'backOfCardImgSrc should match');
        });

        QUnit.module('TarotDeck Shuffling');

        QUnit.test('should shuffle cards', assert => {
            const deck = new TarotDeck(mockImages, 'back.jpg');
            const originalOrder = [...deck.images];
            
            deck.shuffleCards(deck.images);
            
            assert.equal(deck.images.length, originalOrder.length, 'Array length should be preserved');
        });

        QUnit.module('TarotDeck Card Operations');

        QUnit.test('should deal cards correctly', assert => {
            const deck = new TarotDeck(mockImages, 'back.jpg');
            
            const initialStates = deck.getButtonStates();
            assert.true(initialStates.dealEnabled, 'Deal should be enabled initially');
            assert.false(initialStates.backEnabled, 'Back should be disabled initially');

            const states = deck.deal();
            assert.equal(deck.cardsFromIndex, 2, 'cardsFromIndex should be 2 after dealing');
            assert.true(states.backEnabled, 'Back should be enabled after dealing');
        });

        QUnit.test('should go back correctly', assert => {
            const deck = new TarotDeck(mockImages, 'back.jpg');
            
            deck.deal(); // Move to position 2
            const states = deck.back();
            
            assert.equal(deck.cardsFromIndex, 0, 'cardsFromIndex should be 0 after going back');
            assert.false(states.backEnabled, 'Back should be disabled after going back');
        });

        QUnit.test('should reset deck correctly', assert => {
            const deck = new TarotDeck(mockImages, 'back.jpg');
            
            deck.deal(); // Move to position 2
            const states = deck.resetDeck();
            
            assert.equal(deck.cardsFromIndex, 0, 'cardsFromIndex should be 0 after reset');
            assert.false(states.backEnabled, 'Back should be disabled after reset');
            assert.false(states.shuffleEnabled, 'Shuffle should be disabled after reset');
        });

        QUnit.module('TarotDeck Configuration');

        QUnit.test('should handle include trumps correctly', assert => {
            const allImagesWithTrumps = [...mockImages, 'trump1.jpg', 'trump2.jpg'];
            const deck = new TarotDeck(allImagesWithTrumps, 'back.jpg');
            
            deck.setIncludeTrumps(true);
            assert.equal(deck.images.length, allImagesWithTrumps.length, 'Should include all images when trumps enabled');
            
            deck.setIncludeTrumps(false);
            assert.equal(deck.images.length, 56, 'Should use only 56 pip images when trumps disabled');
        });

        QUnit.test('should set number of cards correctly', assert => {
            const deck = new TarotDeck(mockImages, 'back.jpg');
            
            deck.setNumOfCards(3);
            assert.equal(deck.numOfCardsToDeal, 3, 'numOfCards should be 3');
            assert.equal(deck.cardsFromIndex, 0, 'cardsFromIndex should be 0 after setting num cards');
        });

        QUnit.module('TarotDeck Card Retrieval');

        QUnit.test('should get current cards correctly', assert => {
            const deck = new TarotDeck(mockImages, 'back.jpg');
            deck.setNumOfCards(2);
            
            const cards = deck.getCurrentCards();
            assert.equal(cards.length, 2, 'Should return 2 cards');
            assert.ok(cards[0].src !== undefined, 'Card 0 should have src');
            assert.ok(cards[0].caption !== undefined, 'Card 0 should have caption');
            assert.equal(cards[0].caption, 1, 'Card 0 caption should be 1');
            assert.equal(cards[1].caption, 2, 'Card 1 caption should be 2');
        });

        QUnit.test('should detect when more cards can be dealt', assert => {
            const deck = new TarotDeck(mockImages, 'back.jpg');
            deck.setNumOfCards(3);
            
            assert.true(deck.moreCardsToDeal(), 'Should have more cards to deal initially');
            
            deck.deal(); // Move to position 3
            assert.true(deck.moreCardsToDeal(), 'Should still have more cards');
            
            // Deal multiple times to reach near end
            for (const _ of Array(25)) {
                deck.deal();
            }
            assert.false(deck.moreCardsToDeal(), 'Should have no more cards at end');
        });

        QUnit.test('should handle edge case for 3 cards with uneven deck', assert => {
            // Use only pip cards (56) - 56 % 3 = 2, so last deal will have uneven cards
            const pipCardsOnly = mockImages.slice(0, 56);
            const deck = new TarotDeck(pipCardsOnly, 'back.jpg');
            deck.setNumOfCards(3);
            
            // Deal until near the end (56 cards / 3 per deal = 18 full deals, 2 cards left)
            for (const _ of Array(18)) {
                deck.deal();
            }
            
            const cards = deck.getCurrentCards();
            
            assert.equal(cards.length, 3, 'Should return 3 cards');
            assert.equal(cards[2].src, 'back.jpg', 'Third card should be back of card due to uneven division');
            assert.equal(cards[2].caption, '', 'Third card should have empty caption');
        });

        QUnit.module('TarotDeck Edge Cases');

        QUnit.test('should handle back button when at start', assert => {
            const deck = new TarotDeck(mockImages, 'back.jpg');
            
            const states = deck.back();
            assert.equal(deck.cardsFromIndex, 0, 'Should stay at 0');
            assert.false(states.backEnabled, 'Back should remain disabled');
        });

        QUnit.test('should handle deal when no more cards available', assert => {
            // Use exactly 56 cards to match the pipImages logic
            const exactly56Cards = Array.from({length: 56}, (_, i) => `card-${i + 1}.jpg`);
            const deck = new TarotDeck(exactly56Cards, 'back.jpg');
            deck.setNumOfCards(2);
            
            // Deal until the very end (56 cards / 2 per deal = 28 deals, but last valid index is 54)
            for (const _ of Array(27)) {
                deck.deal();
            }
            
            // Last valid deal (shows cards 55 and 56)
            deck.deal();
            assert.equal(deck.cardsFromIndex, 54, 'Should be at 54 after final deal (showing cards 55-56)');
            
            // Try to deal when no more cards available
            const states = deck.deal();
            assert.equal(deck.cardsFromIndex, 54, 'Should stay at 54 when no more cards available');
            assert.false(states.dealEnabled, 'Deal should be disabled');
        });

        QUnit.test('should handle button states correctly throughout lifecycle', assert => {
            // Use 56 cards to match the pipImages logic
            const exactly56Cards = Array.from({length: 56}, (_, i) => `card-${i + 1}.jpg`);
            const deck = new TarotDeck(exactly56Cards, 'back.jpg');
            
            let states = deck.getButtonStates();
            assert.true(states.dealEnabled, 'Deal enabled initially');
            assert.false(states.backEnabled, 'Back disabled initially');
            assert.false(states.shuffleEnabled, 'Shuffle disabled initially');
            
            deck.deal();
            states = deck.getButtonStates();
            assert.true(states.dealEnabled, 'Deal still enabled');
            assert.true(states.backEnabled, 'Back now enabled');
            assert.true(states.shuffleEnabled, 'Shuffle now enabled');
            
            // Deal until near the end (25 more deals = total 26 deals, index = 52, 4 cards left)
            for (const _ of Array(25)) {
                deck.deal();
            }
            states = deck.getButtonStates();
            assert.true(states.dealEnabled, 'Deal still enabled near end (4 cards remaining: 52+2=54 < 56)');
            assert.true(states.backEnabled, 'Back still enabled');
            assert.true(states.shuffleEnabled, 'Shuffle still enabled');
            
            // Deal to last valid position (27th deal, index = 54, 2 cards left)
            deck.deal();
            states = deck.getButtonStates();
            assert.false(states.dealEnabled, 'Deal disabled when exactly 2 cards remaining (54+2=56 !< 56)');
            assert.true(states.backEnabled, 'Back still enabled');
            assert.true(states.shuffleEnabled, 'Shuffle still enabled');
        });
    }
}

// Export for browser use
if (typeof window !== 'undefined') {
    window.TarotDeckTests = TarotDeckTests;
    window.mockImages = mockImages;
}
