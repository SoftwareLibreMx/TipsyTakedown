DROP TYPE IF EXISTS Currency;
CREATE Type Currency AS ENUM ('MXN');

CREATE TABLE PaymentLog (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID NOT NULL,
    payment_amount DOUBLE presition NOT NULL,
    currency Currency NOT NULL,
    transaction_date date not null,
    status text NOT NULL,
    error text DEFAULT NULL,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),
    deleted_at TIMESTAMP DEFAULT NULL,
    CONSTRAINT fk_user_id FOREIGN KEY(user_id) REFERENCES users(id)
);

-- PROMO CODE tables
CREATE TABLE PromoCode (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    code text NOT NULL,
    discount_amount DOUBLE presition NOT NULL,
    discount_percentage DOUBLE presition NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),
    deleted_at TIMESTAMP DEFAULT NULL
);

-- SUBSCRIPTION tables
DROP TYPE IF EXISTS PaymentInterval;
CREATE Type PaymentInterval AS ENUM ('MONTHLY', 'ANUAL');

CREATE TABLE SubscriptionType (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    payment_interval PaymentInvetval NOT NULL,
    currency Currency NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),
    deleted_at TIMESTAMP DEFAULT NULL
)

CREATE TABLE Subscription (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID NOT NULL,
    subscription_type_id UUID NOT NULL,
    payments_log_id UUID NOT NULL,
    promo_code_id UUID DEFAULT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),
    deleted_at TIMESTAMP DEFAULT NULL,
    CONSTRAINT fk_user_id FOREIGN KEY(user_id) REFERENCES users(id),
    CONSTRAINT fk_subscription_type_id FOREIGN KEY(subscription_type_id) REFERENCES subscription_type(id),
    CONSTRAINT fk_payments_log_id FOREIGN KEY(payments_log_id) REFERENCES payment_log(id),
    CONSTRAINT fk_promo_code_id FOREIGN KEY(promo_code_id) REFERENCES promo_code(id)
);
