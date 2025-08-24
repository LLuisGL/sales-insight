import Chart from "chart.js/auto";

const filter_category = document.querySelector('#category');
const filter_sub = document.querySelector('#sub_category');
const filter_state = document.querySelector('#state');
const filter_city = document.querySelector('#city');
const filter_dateS = document.querySelector('#fechaIni');
const filter_dateE = document.querySelector('#fechaFin');

//Función que solo se ejecuta al cargar la página
document.addEventListener('DOMContentLoaded', async () => {
    refreshFilters()

    let body = {
        category: filter_category.value,
        state: filter_state.value,
    }

    fetch("http://localhost:8000/data/filters/", {
            method:'POST', 
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(body)})
    .then((response) => response.json())
    .then((data) => {
        let categories = data.category;
        let sub_categories = data.sub_category;
        let states = data.state;
        let cities = data.city;

        populateSelect(filter_category,categories)

        populateSelect(filter_sub, sub_categories)

        populateSelect(filter_state, states)

        populateSelect(filter_city, cities)
    })
    .catch((err) => console.error("Error cargando datos:", err));
});

//Seteo todos los filtros con un listener
[filter_city,filter_state,filter_sub,filter_category, filter_dateS, filter_dateE].map(item => item.addEventListener('change', (event) => {
    refreshFilters(event);
}));

//Función para refrescar todos los elementos interactivos cuando se selecciona un filtro
function refreshFilters(event){
    let body = {
        category: filter_category.value,
        sub_category: filter_sub.value,
        state: filter_state.value,
        city:filter_city.value,
        start_date:filter_dateS.value != "" ? filter_dateS.value:"All",
        end_date:filter_dateE.value != "" ? filter_dateE.value: "All"
    }

    fetch("http://localhost:8000/data/filters/", {
            method:'POST', 
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(body)})
    .then((response) => response.json())
    .then((data) => {
        let sub_categories = data.sub_category;
        let cities = data.city;

        if(event.target.id == "category") populateSelect(filter_sub, sub_categories)
        
        if(event.target.id == "state") populateSelect(filter_city, cities)
        
    })
    .catch((err) => console.error("Error cargando datos:", err));

    fetch('http://localhost:8000/data/count/', {
            method:'POST', 
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(body)})
        .then(response => response.json())
        .then(data => {
            renderChart(data.map(item => item.category_name), data.map(item => item.category_value), "Ventas por Categoria", "pie", "countChart")
        })
        .catch(err => console.error(err));

    fetch('http://localhost:8000/data/sales/', {
            method:'POST', 
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(body)})
        .then(response => response.json())
        .then(data => {
            const total = document.querySelector('#total');
            total.innerHTML = `$${data.total}`
            renderChart(data.segment.map(item => item.segment_name), data.segment.map(item => item.segment_value), "Ventas Totales ($)", "pie", "salesSegmentChart")
        })
        .catch(err => console.error(err));

    fetch('http://localhost:8000/data/clients/', {
            method:'POST', 
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(body)})
        .then(response => response.json())
        .then(data => {
            const tbody = document.querySelector('#clients_table');
            tbody.innerHTML = "";
            data.forEach(client => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${client.name}</td>
                    <td>${client.segment}</td>
                    <td>${client.city}</td>
                    <td>${client.state}</td>
                    <td>${client.sales}</td>
                `;
                tbody.appendChild(row);
            });
        })
        .catch(err => console.error(err));
    
    fetch('http://localhost:8000/data/products/', {
            method:'POST', 
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(body)})
        .then(response => response.json())
        .then(data => {
            const tbody = document.querySelector('#products_table');
            tbody.innerHTML = "";
            data.forEach(product => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${product.id}</td>
                    <td>${product.name}</td>
                    <td>${product.category}</td>
                    <td>${product.sub_category}</td>
                    <td>${product.sales}</td>
                `;
                tbody.appendChild(row);
            });
        })
        .catch(err => console.error(err));

    fetch("http://localhost:8000/data/charts/", {
        method:'POST', 
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    })
    .then(res => res.json())
    .then(data => renderChart(data.map(item => item.mes), data.map(item => item.total_sales), "Ventas Totales ($)", "line", "salesChart"))
    .catch(err => console.error("Error cargando datos:", err));


}

let charts = {};

//Función usada para dibujar las gráficas que usé dentro
function renderChart(labels_fct, values_fct, dataset_name, type_chart, chart_name) {
    const ctx = document.getElementById(chart_name).getContext("2d");

    if (charts[chart_name]) {
        charts[chart_name].destroy();
    }

    charts[chart_name] = new Chart(ctx, {
        type: type_chart,
        data: {
            labels: labels_fct,
            datasets: [{
                label: dataset_name,
                data: values_fct,
                backgroundColor: type_chart != "pie" ? "rgba(54, 162, 235, 0.6)":[
                'rgb(255, 99, 132)',
                'rgb(54, 162, 235)', 
                'rgb(255, 205, 86)'  
            ],
                borderColor: type_chart != "pie" ? "rgba(54, 162, 235, 1)": "rgba(0,0,0,0)",
                borderWidth: 1,
            }],
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: true, position: "top" },
                title: { display: true, text: "Grafico Fecha VS Ventas" },
            },
        },
    });
}

//Función usada para restaurar los elementos de tipo "select" a su optiòn principaal
function populateSelect(selectElement, items) {
    const firstOption = selectElement.options[0];

    selectElement.innerHTML = "";

    if (firstOption) selectElement.appendChild(firstOption);

    items.forEach(item => {
        const option = document.createElement('option');
        option.value = item;
        option.textContent = item;
        selectElement.appendChild(option);
    });
}

//Esta función es para el botón de "Ventas"
const modal = document.getElementById("modal");
  const openModal = document.getElementById("ventas-btn");
  const closeModal = document.getElementById("closeModal");

  openModal.addEventListener("click", () => {
    modal.classList.remove("hidden");
    modal.classList.add("flex"); 
  });

  closeModal.addEventListener("click", () => {
    modal.classList.add("hidden");
    modal.classList.remove("flex");
  });

  modal.addEventListener("click", (e) => {
    if (e.target === modal) {
      modal.classList.add("hidden");
      modal.classList.remove("flex");
    }
  });