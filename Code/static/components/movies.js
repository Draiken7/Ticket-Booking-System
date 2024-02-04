const movies = {
    template: `
<div>
<div class="container">
    <div class="row bg-transparent text-white">
        <div>
            <router-link to='/admin'>
                <button class="btn btn-outline-info" title="Back">
                    <i class="bi bi-skip-backward fs-1"></i>
                </button>
            </router-link>
        </div>
        <div class="header text-center text-dark">
            <h2>MOVIE MANAGEMENT</h2>
        </div>
        <div class="mx-auto my-2">
            <button class="btn btn-outline-primary" @click="toggleadd" title="Add New Movie">
                <i class="bi bi-plus-square fs-1"></i>
            </button>
        </div>
    </div>
    <div id="hiderif" v-if="this.add">
        <h3>Add Movie Details</h3>
        <p class="text-danger" v-if="this.message">{{this.message}}</p>
        <button class="btn btn-secondary my-2" @click="toggleadd" title="Cancel">
            <i class="bi bi-x fs-2"></i>
        </button>
        <div class="mb-3">
            <input type="text" placeholder="Name" class="form-control" v-model="form.name">
        </div>
        <div class="mb-3">
            <input type="text" placeholder="Rating" class="form-control" v-model="form.Rating">
        </div>
        <div class="mb-3">
            <input type="text" placeholder="userRating" classs="form-control" v-model="form.userRating">
        </div>
        <div class="mb-3">
            <input type="text" placeholder="Tags" classs="form-control" v-model="form.tags">
        </div>
        <div class="mb-3">
            <p class="text-danger">This Field CANNOT be updated later!</p>
            <input type="time" placeholder="userRating" classs="form-control" v-model="form.duration">
        </div>
        <div class="mb-3">
            <button v-bind:class="this.button" @click="addMovie" title="click to Add">
                <i class="bi bi-node-plus fs-2"></i>
            </button>
        </div>
    </div>
    <div id="hiderelse" v-else>
        <div v-if="this.data.length > 0" class="row">
            <div class="accordion">
                <div v-for="(movie, index) in this.data" class="accordion-item bg-dark text-white">
                    <h2 class="accordion-header" :id="'panelsStayOpen-heading-'+index">
                        <button class="accordion-button" type="button" data-bs-toggle="collapse"
                            :data-bs-target="'#panelsStayOpen-collapse-'+index" aria-expanded="true"
                            :aria-controls="'panelsStayOpen-collapse-'+index">
                            <h3>{{movie.name}}</h3>
                        </button>
                    </h2>
                    <div :id="'panelsStayOpen-collapse'-index" class="accordion-collapse collapse show"
                        :aria-labelledby="'panelsStayOpen-heading'+index">
                        <div class="accordion-body">
                            <div>
                                <div>
                                    <p v-if="movie.userRating"><strong>User Rating:</strong> {{movie.userRating}}</p>
                                    <p v-if="movie.rating"><strong>Rating:</strong> {{movie.rating}}</p>
                                    <p v-if="movie.tags"><strong>Tags:</strong> {{movie.tags}}</p>
                                    <p v-if="movie.duration"><strong>Duration:</strong> {{movie.duration}}</p>
                                </div>
                            </div>
                            <div v-if="update">
                                <button class="btn btn-secondary" @click="toggleupdate">
                                    <i class="bi bi-x fs-2"></i>
                                </button>
                                <div class="mb-3">
                                    <input type="text" v-bind:placeholder="movie.name" class="form-control"
                                        v-model="form.name">
                                </div>
                                <div class="mb-3">
                                    <input type="number" v-bind:placeholder="movie.userRating" class="form-control"
                                        v-model="form.userRating">
                                </div>
                                <div class="mb-3">
                                    <input type="text" v-bind:placeholder="movie.rating" classs="form-control"
                                        v-model="form.rating">
                                </div>
                                <div class="mb-3">
                                    <input type="number" v-bind:placeholder="movie.tags" classs="form-control"
                                        v-model="form.tags">
                                </div>
                                <div class="mb-3">
                                    <button class="btn btn-outline-primary" @click="updater(movie.id)"
                                        title="Click to Update">
                                        <i class="bi bi-clipboard-plus fs-2"></i>
                                    </button>
                                </div>
                            </div>
                            <div>
                                <button class="btn btn-outline-warning" @click="toggleupdate" title="Update">
                                    <i class="bi bi-pencil-square fs-3"></i>
                                </button>
                                <span v-if="movie.shows.length>0">
                                    <p>There are currently active Shows for this movie!</p>
                                    <button class="btn btn-outline-secondary" disabled>
                                        <i class="bi bi-trash3 fs-2"></i>
                                    </button>
                                </span>
                                <span v-else>
                                    <button class="btn btn-outline-danger" @click="remove(movie.id)" title="Delete">
                                        <i class="bi bi-trash3 fs-2"></i>
                                    </button>
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
</div>
    `,
    data() {
        return {
            data: null,
            add: false,
            form: {
                name: null,
                rating: null,
                userRating: null,
                tags: null,
                duration: null
            },
            message: null,
            error: false,
            update: false,
            button: "btn btn-outline-primary",
            buttonup: "btn btn-outline-primary"
        }
    },
    methods: {
        toggleadd() {
            this.add = !this.add
        },
        toggleupdate() {
            this.update = !this.update
        },
        addMovie() {
            this.button = "btn btn-warning"
            this.message = null
            this.error = false
            if (!this.form.name) {
                this.message = "name cannot be empty"
            }
            else if (!this.form.duration) {
                this.message = "duration cannot be empty"
            }
            // else if(!this.form.capacity){
            //     this.message = "Capacity cannot be empty!"
            // }
            else {
                if (this.data.length > 0) {
                    for (var x of this.data) {
                        if (x.name == this.form.name) {
                            this.error = true
                            this.message = "Movie with same name exists!"
                            break
                        }
                    }
                }
                if (!this.error) {
                    this.form.tags = this.form.tags ? this.form.tags : ""
                    this.form.rating = this.form.rating ? this.form.rating : ""
                    this.form.userRating = this.form.userRating ? this.form.userRating : null
                    fetch('http://127.0.0.1:5000/movie', {
                        method: "POST",
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': 'Bearer ' + localStorage.getItem('auth-token')
                        },
                        body: JSON.stringify(this.form)
                    }).then((res) => res.json()).then((data) => {
                        console.log(data)
                        this.message = data.message
                        this.button = "btn btn-success"

                        this.data.push({
                            "id": data.id,
                            "name": this.form.name,
                            "rating": this.form.rating,
                            "userRating": this.form.userRating,
                            "tags": this.form.tags,
                            "duration": this.form.duration
                        })
                    }).catch((error) => {
                        console.log(error)
                    })
                }
            }
            this.form.name = null
            this.form.duration = null
            this.form.tags = null
            this.form.userRating = null
            this.form.rating = null
            this.button = "btn btn-primary"
            this.error = false
        },
        async remove(id) {
            const res = await fetch('http://127.0.0.1:5000/movie/' + id, {
                method: "DELETE",
                headers: {
                    "Authorization": "Bearer " + localStorage.getItem('auth-token')
                }
            })
            const data = await res.json()
            if (res.status == 200) {
                this.data = this.data.filter(x => x.id != id)
            }
        },
        async updater(id) {
            var a = this.data.find(x => (x.id == id))
            if (!this.form.name) {
                this.form.name = a.name
            }
            if (!this.form.rating) {
                this.form.rating = a.rating
            }
            if (!this.form.userRating) {
                this.form.userRating = a.userRating
            }
            if (!this.form.tags) {
                this.form.tags = a.tags
            }
            this.form.duration = a.duration
            let x = this.form
            x.id = id
            const res = await fetch('http://127.0.0.1:5000/movie/' + id, {
                method: "PUT",
                body: JSON.stringify(x),
                headers: {
                    'Content-Type': 'application/json',
                    "Authorization": "Bearer " + localStorage.getItem('auth-token')
                }
            })
            const data = await res.json()
            if (res.status == 200){
                this.data = this.data.map(x => {
                    if(x.id==id){
                        x = this.form
                        x.id = id
                    }
                    return x
                })
            }
        }
    },
    async created() {
        const response = await fetch('http://127.0.0.1:5000/movie', {
            methods: 'GET',
            headers: {
                'Authorization': 'Bearer ' + localStorage.getItem('auth-token')
            }
        })
        this.data = await response.json()
    },
}
export default movies