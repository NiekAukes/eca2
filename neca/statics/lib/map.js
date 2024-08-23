function leaflet(id, config = {}) {
    const element = document.getElementById(id);

    // create the map, and set the view to the default location
    let default_location = config.location || [52.221539, 6.893662];
    let default_zoom = config.zoom || 12.25;
    let m = L.map('map').setView(default_location, default_zoom);
    
    // create an entity map to store the entities created
    let entities = {};

    // if an onclick event is specified, add it
    if (config.onClick) {
        m.on("click", config.onClick);
    }

    // add the OpenStreetMap tiles
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
        ...config.leafletOptions || {}
    }).addTo(m);

    function onEvent(data) {
        // available actions: 
        // - draw
        //   - marker
        //   - circle
        //   - line
        //   - polygon
        // - remove
        // - setEntityPosition
        // - setView

        // draw requires a type, coordinates, a name, and optionally a style
        // remove requires a name
        // setEntityPosition requires a name and coordinates
        // setView requires coordinates and a zoom level
    
        if (data.action === "draw") {
            if (entities.hasOwnProperty(data.name)) {
                // remove the entity if it already exists
                entities[data.name].remove();
            }

            if (data.type === "marker") {
                entities[data.name] = drawMarker(data.coordinates, data.options || {});
            }
            else if (data.type === "circle") {
                entities[data.name] = drawCircle(data.coordinates, data.options || {});
            }
            else if (data.type === "line") {
                entities[data.name] = drawLine(data.coordinates, data.options || {});
            }
            else if (data.type === "polygon") {
                entities[data.name] = drawPolygon(data.coordinates, data.options || {});
            }
        }
        else if (data.action === "remove") {
            entities[data.name].remove();
            delete entities[data.name];
        }
        else if (data.action === "setEntityPosition") {
            entities[data.name].setLatLng(data.coordinates);
        } 
        else if (data.action === "setView") {
            m.setView(data.coordinates, data.zoom);
        }
    }

    function addEventListener(event, callback) {
        m.on(event, callback);
    }

    function drawMarker(coordinates, options) {
        let marker = L.marker(coordinates, {...options}).addTo(m);
        return marker;
    }
    
    function drawCircle(coordinates, radius, options) {
        let circle = L.circle(coordinates, {radius: radius, weight:5, 'opacity':0.65, ...options}).addTo(m);
        return circle;
    }
    function drawLine(coordinates, options) {
        let line = L.polyline(coordinates, {weight:5, 'opacity':0.65, ...options}).addTo(m);
        return line;
    }
    function drawPolygon(coordinates, options) {
        let polygon = L.polygon(coordinates, {weight:5, 'opacity':0.65, ...options}).addTo(m);
        return polygon;
    }

    function addEntity(name, entity) {
        entities[name] = entity;
    }

    function getEntity(name) {
        return entities[name];
    }

    function removeEntity(name) {
        entities[name].remove();
        delete entities[name];
    }

    return {
        // functions to expose
        onEvent: onEvent,
        addEventListener: addEventListener,

        // drawing functions
        drawMarker: drawMarker,
        drawCircle: drawCircle,
        drawLine: drawLine,
        drawPolygon: drawPolygon,

        // entity functions
        addEntity: addEntity,
        getEntity: getEntity,
        removeEntity: removeEntity,

        // internal map
        map: m,
    }
}