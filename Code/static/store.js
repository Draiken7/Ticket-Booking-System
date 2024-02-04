const state = {
    theaters:null,
    movies: null,
    tid:null,
    mid:null,
    queryparam:null,
    sid: null,
}

const store = new Vuex.Store({
    state,
    getters:{
        gettheaters(state){
            return state.theaters
        },
        getmovies(state){
            return state.movies
        },
        getTID(state){
            return state.tid
        },
        getMID(state){
            return state.mid
        },
        getQueryParam(state){
            return state.queryparam
        },
        getSID(state){
            return state.sid
        }
    },
    mutations:{
        setTheaters(state, data){
            state.theaters = data
        },
        setMovies(state, data){
            state.movies = data
        },
        setID(state, id){
            state.tid = id
        },
        setMID(state, id){
            state.mid = id
        },
        setQueryParam(state, str){
            state.queryparam = str
        },
        setSID(state, id){
            state.sid = id
        }
    }
})
 export default store