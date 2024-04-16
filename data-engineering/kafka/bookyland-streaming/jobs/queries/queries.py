from pyspark.sql.functions import col


def filter_by_payment_status(df, payment_status:str):
    """ 
        Retrieve all records based on payment_status
    """
    return df.filter(col('payment_status') == payment_status)

def filter_by_payment_method(df, payment_type):
    """
        Retrieve all records based on payment method 
    """
    return df.filter(
        col('payment_type') == payment_type
    )

def group_by_city_and_payment_status(df,payment_status):
    df_r = filter_by_payment_method(df=df,payment_type=payment_status)
    df_r = df_r.groupBy('user_city').count()
    return df_r