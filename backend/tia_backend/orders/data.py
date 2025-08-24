import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .database.db import get_connection

def get_where_query(data, get_filter=False, pie_mode=False):
    filters = []
    params = []

    category = data.get('category')
    sub_category = data.get('sub_category')
    state = data.get('state')
    city = data.get('city')
    start_date = data.get('start_date')
    end_date = data.get('end_date')

    if(get_filter):
        return [category, state]

    if category and category != "All" and not pie_mode:
        filters.append("ms.category = %s")
        params.append(category)

    if sub_category and sub_category != "All" and not pie_mode:
        filters.append("ms.sub_category = %s")
        params.append(sub_category)

    if state and state != "All":
        filters.append("ms.state = %s")
        params.append(state)

    if city and city != "All":
        filters.append("ms.city = %s")
        params.append(city)
    
    if (start_date and end_date) and (start_date != "All"and end_date != "All"):
        filters.append("ms.order_date BETWEEN %s AND %s")
        params.append(start_date)
        params.append(end_date)

    where_query = ""
    if filters:
        where_query = "WHERE " + " AND ".join(filters)

    return [where_query,params]

@csrf_exempt
def best_clients(request):
    data = json.loads(request.body)

    where_query, params = get_where_query(data)

    query = f"SELECT customer_id, customer_name, segment, MAX(ms.city) AS city, MAX(ms.state) AS state, SUM(ms.sales) AS total_sales FROM master_sales AS ms {where_query if where_query != "WHERE" else ""} GROUP BY ms.customer_name, ms.segment, customer_id ORDER BY total_sales DESC LIMIT 20"
    conn = get_connection()
    orders = []
    with conn.cursor() as cur:
        cur.execute(query, params)
        for order in cur.fetchall():
            orders.append(
                {
                    'name': order[1],
                    'segment': order[2],
                    'city': order[3],
                    'state': order[4],
                    'sales': order[5]
                }
            )
    
    return JsonResponse(orders, safe=False)

@csrf_exempt
def best_products(request):
    data = json.loads(request.body)

    where_query, params = get_where_query(data)

    query = f"SELECT ms.product_id, ms.category, ms.sub_category, MAX(ms.product_name) AS product_name, COUNT(ms.product_id) AS total_ventas FROM master_sales AS ms {where_query if where_query != "WHERE" else ""} GROUP BY ms.product_id, ms.category, ms.sub_category ORDER BY total_ventas DESC LIMIT 10"
    conn = get_connection()
    conn = get_connection()
    orders = []
    with conn.cursor() as cur:
        cur.execute(query,params)
        for order in cur.fetchall():
            orders.append(
                {
                    'id': order[0],
                    'category': order[1],
                    'sub_category': order[2],
                    'name': order[3],
                    'sales': order[4],
                }
            )
    
    return JsonResponse(orders, safe=False)

@csrf_exempt
def chart_generator(request):
    data = json.loads(request.body)

    where_query, params = get_where_query(data)

    query = f"select DATE_TRUNC('month', ms.order_date)::DATE AS mes, SUM(ms.sales) FROM master_sales AS ms {where_query if where_query != "WHERE" else ""} GROUP BY mes ORDER BY mes ASC"
    conn = get_connection()
    orders = []
    with conn.cursor() as cur:
        cur.execute(query, params)
        for mes in cur.fetchall():
            orders.append(
                {
                    'mes': mes[0],
                    'total_sales': mes[1]
                }
            )

    return JsonResponse(orders, safe=False)

@csrf_exempt
def get_filters(request):
    data = json.loads(request.body)

    category, state = get_where_query(data, get_filter=True)

    conn = get_connection()
    filters = {}
    with conn.cursor() as cur:
        cur.execute("SELECT ms.category FROM master_sales AS ms GROUP BY ms.category ORDER BY ms.category ASC")
        categories = []
        for category_tmp in cur.fetchall():
            categories.append(category_tmp[0])
        
        query = f"SELECT ms.sub_category FROM master_sales AS ms {"WHERE ms.category = %s" if category != "All" else ""} GROUP BY ms.sub_category ORDER BY ms.sub_category ASC"
        cur.execute(query, (category,))
        sub_categories = []
        for sub_category in cur.fetchall():
            sub_categories.append(sub_category[0])
        
        cur.execute("SELECT ms.state FROM master_sales AS ms GROUP BY ms.state ORDER BY ms.state ASC")
        states = []
        for state_tmp in cur.fetchall():
            states.append(state_tmp[0])

        query = f"SELECT ms.city FROM master_sales AS ms {"WHERE ms.state = %s" if state != "All" else ""} GROUP BY ms.city ORDER BY ms.city ASC"
        cur.execute(query, (state,))
        cities = []
        for city in cur.fetchall():
            cities.append(city[0])
        
        filters = {
            'category': categories,
            'sub_category': sub_categories,
            'state': states,
            'city': cities
        }
    return JsonResponse(filters, safe=False)

@csrf_exempt
def get_sales_info(request):
    data = json.loads(request.body)

    where_query, params = get_where_query(data)
    where_query_total, params_total = get_where_query(data)

    conn = get_connection()
    query = f"SELECT sum(ms.sales) FROM master_sales AS ms {where_query_total if where_query_total != "WHERE" else ""}"
    conn = get_connection()
    orders = {}
    with conn.cursor() as cur:
        cur.execute(query, params_total)
        orders['total'] = cur.fetchone()[0]
        orders['segment'] = []
        query = f"SELECT segment, sum(ms.sales) FROM master_sales AS ms {where_query if where_query != "WHERE" else ""} GROUP BY ms.segment"
        cur.execute(query, params)
        for segment_tmp in cur.fetchall():
            orders['segment'].append({
                'segment_name': segment_tmp[0],
                'segment_value': segment_tmp[1]
            })

    return JsonResponse(orders, safe=False)

@csrf_exempt
def get_sales_count(request):
    data = json.loads(request.body)

    where_query, params = get_where_query(data, pie_mode=True)

    conn = get_connection()
    query = f"SELECT ms.category, COUNT(ms.row_id) FROM master_sales AS ms {where_query if where_query != "WHERE" else ""} GROUP BY ms.category"
    orders = []
    with conn.cursor() as cur:
        
        cur.execute(query, tuple(params))
        for segment_tmp in cur.fetchall():
            orders.append({
                'category_name': segment_tmp[0],
                'category_value': segment_tmp[1]
            })

    return JsonResponse(orders, safe=False)