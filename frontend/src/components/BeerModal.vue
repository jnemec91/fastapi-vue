<template>
    <div class="backdrop" @click="$emit('closeBeerModal')"></div>
    <div class="modal">
        <h2>{{ beer.name }}</h2>
        <p>{{ beer.style }}</p>
        <div class="modal-content">
            <div class="beer-stats-div">
                <div class="beer-ball">
                    <p>ABV</p>
                    <p>{{ beer.abv }}</p>
                </div>
                <div class="beer-ball">
                    <p>EPM</p>
                    <p>{{ beer.epm }}</p>
                </div>
                <div class="beer-ball"></div>                
                <div class="beer-ball">
                    <p>Rating</p>
                    <p>{{ beer.rating }}</p>
                </div>
                <div class="beer-ball"></div>
                <div class="beer-ball"></div> 
                <div class="beer-square">
                    <p>{{ beer.brewery }}</p>
                    <p>{{ beer.location }}</p>
                </div>
            </div>
            <div class="review-div">
                <p v-if="beer.description">{{ beer.description }}</p>
                <p v-else>Bez popisu výrobce.</p>
            </div>
        </div>
        <div class="source-div">
            <p>Data stažena z:</p>
            <a :href="beer.url">{{ beer.url }}</a>
        </div>
        <hr>
        <button @click="$emit('closeBeerModal')" class="scraper-button modal-button">Zavřít</button>
    </div>
</template>

<script>
export default {
    name: 'BeerModal',
    props: ['beer']
}
</script>

<style>
    .backdrop {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.3);
    }

    .modal {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.26);
        z-index: 2;
        max-height: 80vh;
        overflow-y: scroll;
        scrollbar-width: thin;
        scrollbar-color:#f28e1c white ;        
    }
    .modal-content {
        justify-content: space-between;
        width: 100%;
    }
    .review-div {
        transform: translateX(2px);
        width: 400px;
        min-height: 400px;
        padding: 10px;
        border: 2px solid black;
        border-radius: 0 0 12px 12px;
        color: white;
        background: #f28e1c;
        font-weight: bold;
        font-size: large;
        margin: auto;
    }
    .beer-stats-div {
        margin: 135px auto 60px auto;
        padding: 10px;
        width: 400px;
        position: relative;
    }
    .source-div {
        width: 100%;
    }

    .beer-ball{
        border-radius: 50%;
        width: 100px;
        height: 100px;
        background: white;
        border-top: 2px solid black;
        position: absolute;
    }
    .beer-ball:nth-of-type(1){
        top: -70px;
        left: 0;
        transform: rotateZ(316deg);
    }
    .beer-ball:nth-of-type(2){
        top: -110px;
        left: 55px;
        transform: rotateZ(351deg);
    }
    .beer-ball:nth-of-type(3){
        top: -110px;
        left: 130px;
        transform: rotateZ(356deg);
    }
    .beer-ball:nth-of-type(5){
        top: -110px;
        left: 190px;
        transform: rotateZ(18deg);
    }
    .beer-ball:nth-of-type(4){
        top: -110px;
        left: 270px;
        transform: rotateZ(10deg);
    }     
    .beer-ball:nth-of-type(6){
        top: -70px;
        left: 325px;
        transform: rotateZ(39deg);
    }         
    .beer-square{
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        background: white;
        border-right: 2px solid black;
        border-left: 2px solid black;
        border-bottom: 2px solid black;
    }
    .modal-button{
        margin: 10px auto;
    }
</style>