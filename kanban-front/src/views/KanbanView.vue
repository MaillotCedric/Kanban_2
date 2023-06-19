<template>
    <div class="kanban">
        <!-- Modal : modification titre -->
        <div class="modal fade" id="modal_form" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabel"></h5> <!-- Modal label injected via JS -->
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <form>
                        <div class="form-group">
                            <input type="text" class="form-control" id="input_titre" placeholder="Veuillez entrer un titre ..." v-model="titre" @input="handle_btn">
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-primary my-btn" @click="save_titre" v-show="btn_visible">Enregistrer</button>
                </div>
                </div>
            </div>
        </div>

        <button class="btn btn-primary my-btn btn-action" data-toggle="modal" data-target="#modal_form_tache">
            <i class="bi bi-list-task"></i>
            Ajouter une tâche
        </button>

        <button class="btn btn-primary my-btn btn-action" data-toggle="modal" data-target="#modal_form_colonne">
            <i class="bi bi-columns"></i>
            Ajouter une colonne
        </button>

        <!-- Modal : ajout tâche -->
        <div class="modal fade" id="modal_form_tache" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabel">Ajouter une tâche</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <form>
                        <div class="form-group">
                            <select id="select-colonne" class="custom-select" v-model="selected_column">
                                <option selected>Open this select menu</option>
                                <option value="1">One</option>
                                <option value="2">Two</option>
                                <option value="3">Three</option>
                            </select>
                        </div>

                        <div class="form-group" v-if="selected_column !== ''">
                            <input type="text" class="form-control" id="input_titre_tache" placeholder="Veuillez entrer un titre ..." v-model="titre">
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button v-if="titre !== ''" type="button" class="btn btn-primary my-btn" @click="add_tache">Enregistrer</button>
                </div>
                </div>
            </div>
        </div>

        <!-- Modal : ajout colonne -->
        <div class="modal fade" id="modal_form_colonne" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabel">Ajouter une colonne</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <form>
                        <div class="form-group">
                            <input type="text" class="form-control" id="input_titre_colonne" placeholder="Veuillez entrer un titre ..." v-model="titre">
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-primary my-btn" @click="add_colonne" v-if="titre !== ''">Enregistrer</button>
                </div>
                </div>
            </div>
        </div>

        <div id="jk-container"></div>
    </div>
</template>

<script lang="ts">
    import * as tb from "../scripts/toolbox"
    import axios from "axios";

    export default {
        data() {
            return {
                my_kanban: null,
                boards: [],
                titre: "",
                board_id: "",
                id_tache: "",
                btn_visible: true,
                colonne: false,
                tache: false,
                selected_column: ""
            }
        },
        methods: {
            add_colonne() {
                axios
                    .get("/api/colonnes/")
                    .then((response) => {
                        let position_colonne = String(tb.sorted_columns(response.data.results).slice(-1)[0].position_colonne + 1)
                        let titre_colonne = this.titre
                        let data = {
                            position_colonne,
                            titre_colonne
                        }
                        
                        axios
                            .post("/api/colonnes/", data)
                            .then((response) => {
                                this.my_kanban.addBoards(
                                    axios
                                        .get("/api/colonnes/")
                                        .then((response) => {
                                            let id_colonne = String(tb.sorted_columns(response.data.results).slice(-1)[0].id_colonne)
                                            let colonnes = tb.sorted_columns(response.data.results)
                                            let select_colonne = document.getElementById("select-colonne")
                                            let board = {
                                                "id": "board-id-" + id_colonne,
                                                "title": titre_colonne,
                                                "item": []
                                            }

                                            this.my_kanban.addBoards([board])
                                            // @ts-ignore
                                            select_colonne.innerHTML = `<option value="" selected>Selectionner un colonne</option>`
                                            colonnes.forEach((colonne, index) => {
                                                // @ts-ignore
                                                select_colonne.innerHTML += `<option value="`+ colonne.id_colonne +`">`+ colonne.titre_colonne +`</option>`
                                            });
                                            this.set_headers_icons()
                                            
                                        })
                                        .catch((error) => {
                                            tb.print_(error)
                                        })
                                )
                            })
                            .catch((error) => {
                                tb.print_(error)
                            })
                    })
                    .catch((error) => {
                        tb.print_(error)
                    })
                // @ts-ignore
                $('#modal_form_colonne').modal('hide')
            },
            add_tache() {
                axios
                    .get("/api/colonnes/"+ this.selected_column +"/")
                    .then((response) => {
                        let position_tache = String(response.data.taches.length + 1)
                        let data = {
                            "titre_tache": this.titre,
                            "position_tache": position_tache,
                            "colonne": this.selected_column
                        }

                        axios
                            .post("/api/taches/", data)
                            .then((response) => {
                                axios
                                    .get("api/taches/")
                                    .then((response) => {
                                        let item_id = response.data.results.length == 0 ? 1 : tb.sorted_taches(response.data.results).slice(-1)[0].id_tache
                                        this.my_kanban.addElement("board-id-" + this.selected_column, {
                                            // title: this.titre
                                            "id": "item-id-" + item_id,
                                            "title": this.titre,
                                            "position": position_tache
                                        });


                                        // @ts-ignore
                                        let titre_tache_container = document.querySelector("[data-eid=item-id-"+ item_id +"]")
                                        let element = null

                                        // @ts-ignore
                                        titre_tache_container.innerHTML = `
                                            <i class="bi bi-pencil-square i-pencil-tache"></i>
                                            <div>
                                                <i class="bi bi-arrows-move i-arrows-tache item_handle"></i> `+ this.titre +`
                                            </div>
                                        `
                                        // @ts-ignore
                                        element = titre_tache_container.getElementsByClassName("i-pencil-tache")[0]
                                        // @ts-ignore
                                        this.set_event_icones_tache(element)
                                    })
                                    .catch((error) => {
                                        tb.print_(error)
                                    })
                            })
                            .catch((error) => {
                                tb.print_(error)
                            })
                        // @ts-ignore
                        $('#modal_form_tache').modal('hide')
                    })
                    .catch((error) => {
                        tb.print_(error)
                    })
            },
            handle_btn() {
                if(this.titre == "") { // l'input est vide
                    this.btn_visible = false // btn hidden
                } else {
                    this.btn_visible = true // btn visible
                }
            },
            save_db(url, data) {
                axios
                    .patch(url, data)
                    .then((response) => {
                        if(this.colonne == true) {
                            // @ts-ignore
                            let titre_colonne_container = document.querySelector("[data-id=board-id-"+ this.board_id +"]").getElementsByClassName("kanban-title-board")[0]

                            axios
                                .get("/api/colonnes/")
                                .then((response) => {
                                    let colonnes = tb.sorted_columns(response.data.results)
                                    let select_colonne = document.getElementById("select-colonne")
                                    

                                    // @ts-ignore
                                    select_colonne.innerHTML = `<option value="" selected>Selectionner un colonne</option>`
                                    colonnes.forEach((colonne, index) => {
                                        // @ts-ignore
                                        select_colonne.innerHTML += `<option value="`+ colonne.id_colonne +`">`+ colonne.titre_colonne +`</option>`
                                    });
                                })
                                .catch((error) => {
                                    tb.print_(error)
                                })

                            // @ts-ignore
                            titre_colonne_container.innerText = this.titre
                            this.colonne = false
                            this.board_id = ""
                        } else {
                            // @ts-ignore
                            let titre_tache_container = document.querySelector("[data-eid=item-id-"+ this.id_tache +"]")
                            let element = null

                            // @ts-ignore
                            titre_tache_container.innerHTML = `
                                <i class="bi bi-pencil-square i-pencil-tache"></i>
                                <div>
                                    <i class="bi bi-arrows-move i-arrows-tache item_handle"></i> `+ this.titre +`
                                </div>
                            `
                            // @ts-ignore
                            element = titre_tache_container.getElementsByClassName("i-pencil-tache")[0]
                            // @ts-ignore
                            this.set_event_icones_tache(element)
                            this.tache = false
                            this.id_tache = ""
                        }
                        this.titre = ""
                    })
                    .catch((error) => {
                        tb.print_(error)
                    })
            },
            get_id(element_id) {
                return element_id.split("-")[2]
            },
            save_titre() {
                let query_params = this.query_params()

                // @ts-ignore
                $('#modal_form').modal('hide')
                if(this.titre !== "") {
                    // @ts-ignore
                    this.save_db(query_params.url, query_params.data)
                }
            },
            query_params() {
                let url = null
                let data = null

                if (this.colonne == true) {
                    // @ts-ignore
                    url = "/api/colonnes/" + this.board_id + "/"
                    // @ts-ignore
                    data = {
                        "titre_colonne": this.titre
                    }
                } else {
                    // @ts-ignore
                    url = "/api/taches/" + this.id_tache + "/"
                    // @ts-ignore
                    data = {
                        "titre_tache": this.titre
                    }
                }

                return { url, data }
            },
            set_headers_icons() {
                // @ts-ignore
                let btn_icones_colonne_containers = document.getElementsByClassName("kanban-title-button")

                // @ts-ignore
                for (let index = 0; index < btn_icones_colonne_containers.length; index++) {
                    // @ts-ignore
                    const element = btn_icones_colonne_containers[index];

                    element.innerHTML = `
                        <i class="bi bi-pencil-square"></i>
                    `
                }
            },
            add_icones_tache() {
                let items_container = document.getElementsByClassName("kanban-item")

                for (let index = 0; index < items_container.length; index++) {
                    const element = items_container[index];
                    element.innerHTML = `
                        <i class='bi bi-pencil-square i-pencil-tache'></i>
                    ` + element.innerHTML
                }
            },
            set_event_icones_tache(htmlElements) {
                let view_model = this

                // @ts-ignore
                $(htmlElements).on('click', view_model, function (e) {
                    // @ts-ignore
                    let data_eid = e.target.parentElement.getAttribute("data-eid")
                    let id_tache = view_model.get_id(data_eid)
                    let titre_tache = e.target.parentElement.innerText
                    let label_container = document.getElementById("exampleModalLabel")
                    let input_titre = document.getElementById("input_titre")
                    
                    // @ts-ignore
                    label_container.innerText = "Modifier le titre de la tâche"
                    // @ts-ignore
                    input_titre.value = titre_tache
                    view_model.titre = titre_tache
                    view_model.id_tache = id_tache
                    view_model.tache = true

                    // @ts-ignore
                    $('#modal_form').modal('show')
                })
            },
            init_kanban() {
                axios
                    .get("/api/colonnes/")
                    .then((response) => {
                        let colonnes = response.data.results
                        let sorted_columns = tb.sorted_columns_on_position(colonnes)
                        let select_colonne = document.getElementById("select-colonne")

                        // @ts-ignore
                        select_colonne.innerHTML = `<option value="" selected>Selectionner un colonne</option>`

                        sorted_columns.forEach((colonne, index) => {
                            let board = {
                                "id": "board-id-" + colonne.id_colonne,
                                "title": colonne.titre_colonne,
                                "item": this.get_items(colonne)
                            }

                            this.boards.push(board)

                            // @ts-ignore
                            select_colonne.innerHTML += `<option value="`+ colonne.id_colonne +`">`+ colonne.titre_colonne +`</option>`
                        });

                        this.create_kanban()
                    })
                    .catch((error) => {
                        tb.print_(error)
                    })
            },
            create_kanban() {
                let icones_colonne_containers = null
                let view_model = this

                // @ts-ignore
                this.my_kanban = new jKanban({
                    element          : '#jk-container',                                           // selector of the kanban container
                    gutter           : '15px',                                       // gutter of the board
                    widthBoard       : '250px',                                      // width of the board
                    responsivePercentage: false,                                    // if it is true I use percentage in the width of the boards and it is not necessary gutter and widthBoard
                    dragItems        : true,                                         // if false, all items are not draggable
                    boards           : this.boards,                                           // json of boards
                    dragBoards       : true,                                         // the boards are draggable, if false only item can be dragged
                    itemAddOptions: {
                        enabled: true,                                              // add a button to board for easy item creation
                        content: '+',                                                // text or html content of the board button   
                        class: 'kanban-title-button btn btn-default btn-xs',         // default class of the button
                        footer: false                                                // position the button on footer
                    },    
                    itemHandleOptions: {
                        enabled             : true,                                 // if board item handle is enabled or not
                        handleClass         : "item_handle",                         // css class for your custom item handle
                        customCssHandler    : "drag_handler",                        // when customHandler is undefined, jKanban will use this property to set main handler class
                        customCssIconHandler: "drag_handler_icon",                   // when customHandler is undefined, jKanban will use this property to set main icon handler class. If you want, you can use font icon libraries here
                        customHandler       : "<i class='bi bi-arrows-move i-arrows-tache item_handle'></i> %title% "  // your entirely customized handler. Use %title% to position item title 
                                                                                            // any key's value included in item collection can be replaced with %key%
                    },
                    view_model: this,
                    click            : function (el) {},                             // callback when any board's item are clicked
                    context          : function (el, event) {},                      // callback when any board's item are right clicked
                    dragEl           : function (el, source) {},                     // callback when any board's item are dragged
                    dragendEl        : function (el) {},                             // callback when any board's item stop drag
                    dropEl           : function (el, target, source, sibling) {
                        let id_tache = view_model.get_id(el.getAttribute("data-eid"))
                        let id_colonne = view_model.get_id(el.offsetParent.getAttribute("data-id"))
                        let id_colonne_source = view_model.get_id(source.offsetParent.getAttribute("data-id"))
                        let position_sibling = null
                        let position_tache = ""

                        if(sibling !== null) {
                            position_sibling = sibling.getAttribute("data-position")
                        }

                        if (position_sibling == "1") {
                            position_tache = "1"
                        } else if(position_sibling == null) {
                            position_tache = String(el.offsetParent.children[1].children.length)
                        } else {
                            if(id_colonne == id_colonne_source) {
                                position_tache = String(parseInt(position_sibling) - 1)
                            } else {
                                position_tache = position_sibling
                            }
                        }

                        axios
                            .patch("api/tache/move/", {
                                "id_tache": id_tache,
                                "colonne": id_colonne,
                                "position_tache": position_tache
                            })
                            .then((response) => {
                                if (id_colonne !== id_colonne_source) {
                                    view_model.refresh_column(id_colonne)
                                    view_model.refresh_column(id_colonne_source)
                                } else {
                                    view_model.refresh_column(id_colonne)
                                }
                            })
                            .catch((error) => {
                                tb.print_(error)
                            })
                    },    // callback when any board's item drop in a board
                    dragBoard        : function (el, source) {},                     // callback when any board stop drag
                    dragendBoard     : function (el) {
                        let id_colonne = view_model.get_id(el.getAttribute("data-id"))
                        let position_colonne = el.getAttribute("data-order")
                        let data = {id_colonne, position_colonne}
                        axios
                            .patch("api/colonne/move/", data)
                            .then((response) => {})
                            .catch((error) => {
                                tb.print_(error)
                            })
                    },                             // callback when any board stop drag
                    buttonClick      : function(el, boardId) {
                        // @ts-ignore
                        let titre_colonne = document.querySelector("[data-id="+ boardId +"]").getElementsByClassName("kanban-title-board")[0].innerText
                        let label_container = document.getElementById("exampleModalLabel")
                        let input_titre = document.getElementById("input_titre")
                        let board_id = this.view_model.get_id(boardId)
                        
                        // @ts-ignore
                        label_container.innerText = "Modifier le titre de la colonne"
                        // @ts-ignore
                        input_titre.value = titre_colonne
                        this.view_model.titre = titre_colonne
                        this.view_model.board_id = board_id
                        this.view_model.colonne = true

                        // @ts-ignore
                        $('#modal_form').modal('show')
                    },                     // callback when the board's button is clicked
                    propagationHandlers: [],                                         // the specified callback does not cancel the browser event. possible values: "click", "context"
                })
                
                this.set_headers_icons()
                this.add_icones_tache()
                // @ts-ignore
                this.set_event_icones_tache($('.i-pencil-tache'))
            },
            get_items(colonne) {
                let sorted_taches = tb.sorted_taches_on_position(colonne.taches)
                let items: any = []
                
                sorted_taches.forEach((tache) => {
                    let item = {
                        "id": "item-id-" + tache.id_tache,
                        "title": tache.titre_tache,
                        "position": tache.position_tache
                    }

                    items.push(item)
                });

                return items
            },
            refresh_column(column_id) {
                let board = document.querySelector("[data-id=board-id-"+ column_id +"]")
                // @ts-ignore
                let main = board.children[1]

                axios
                    .get("api/colonnes/"+ column_id +"/")
                    .then((response) => {
                        let taches = tb.sorted_taches_on_position(response.data.taches)
                        
                        main.innerHTML = "";
                        
                        for (let index = 0; index < taches.length; index++) {
                            const tache = taches[index];

                            main.innerHTML += `
                            <div class="kanban-item" data-eid="item-id-`+ tache.id_tache +`" data-position="`+ tache.position_tache +`" style="cursor: default;">
                                <i class="bi bi-pencil-square i-pencil-tache"></i>
                                <div> <i class="bi bi-arrows-move i-arrows-tache item_handle"></i> `+ tache.titre_tache +`  </div>
                            </div>
                            `
                        }
                        // @ts-ignore
                        this.set_event_icones_tache($('.i-pencil-tache'))
                    })
                    .catch((error) => {[
                        tb.print_(error)
                    ]})
            }
        },
        mounted() {
            let view_model = this
            this.init_kanban()

            // @ts-ignore
            $('#modal_form').on('hidden.bs.modal', view_model, function (e) {
                view_model.btn_visible = true
                view_model.colonne = false
                view_model.tache = false
                view_model.titre = ""
            })

            // @ts-ignore
            $('#modal_form_tache').on('hidden.bs.modal', view_model, function (e) {
                view_model.selected_column = ""
                view_model.titre = ""
            })

            // @ts-ignore
            $('#modal_form_colonne').on('hidden.bs.modal', view_model, function (e) {
                view_model.titre = ""
            })
        }
    }
</script>

<style>
    @media (min-width: 1024px) {
        /* .kanban {
            min-height: 100vh;
            display: flex;
            align-items: center;
        } */
    }
</style>
