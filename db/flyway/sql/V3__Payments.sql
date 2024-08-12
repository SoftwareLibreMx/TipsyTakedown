CREATE TABLE cards (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID NOT NULL,
    card_number text NOT NULL,
    expiration_date date NOT NULL,
    cvv text NOT NULL,
    card_holder_name text NOT NULL,
    zip_code text DEFAULT NULL,
    country text DEFAULT NULL,
    lasts_four_digits text NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),
    deleted_at TIMESTAMP DEFAULT NULL,
    CONSTRAINT fk_user_id FOREIGN KEY(user_id) REFERENCES users(id)
);

DROP TYPE IF EXISTS Currency;
CREATE Type Currency AS ENUM ('MXN', 'USD');

DROP TYPE IF EXISTS PaymentStatus;
CREATE Type PaymentStatus AS ENUM (
    'PENDING', 
    'APPROVED', 
    'REJECTED'
);

DROP TYPE IF EXISTS RejectionReason;
CREATE Type RejectionReason AS ENUM (
    'INSUFFICIENT_FUNDS',
    'INVALID_CARD',
    'INVALID_CVV',
    'INVALID_EXPIRATION_DATE',
    'INVALID_CARD_HOLDER_NAME',
    'INVALID_ZIP_CODE',
    'INVALID_AMOUNT',
    'INVALID_CURRENCY',
    'INVALID_COUNTRY',
    'DISABLED_CARD',
    'BLACKLISTED_CARD',
    'UNSUPPORTED_CARD'
);

DROP TYPE IF EXISTS PaymentMethod;
CREATE Type PaymentMethod AS ENUM (
    'CREDIT_CARD', 
    'DEBIT_CARD',
    'MERCADO_PAGO',
    'CASH',
    'ATM',
    'SPEI_TRANSFER'
);

CREATE TABLE payment_audit_logs (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID NOT NULL,
    payment_amount DOUBLE precision NOT NULL,
    currency Currency NOT NULL,
    transaction_date date not null,
    status PaymentStatus NOT NULL,
    rejection_reason RejectionReason DEFAULT NULL,
    payment_method PaymentMethod NOT NULL,
    card_id UUID NOT NULL,
    error text DEFAULT NULL,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),
    deleted_at TIMESTAMP DEFAULT NULL,
    CONSTRAINT fk_user_id FOREIGN KEY(user_id) REFERENCES users(id),
    CONSTRAINT fk_card_id FOREIGN KEY(card_id) REFERENCES cards(id)
);

-- PROMO CODE tables
CREATE TABLE promo_codes (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    code text NOT NULL,
    discount_amount DOUBLE precision NOT NULL,
    discount_percentage DOUBLE precision NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),
    deleted_at TIMESTAMP DEFAULT NULL
);

-- SUBSCRIPTION tables
DROP TYPE IF EXISTS PaymentCycle;
CREATE Type PaymentCycle AS ENUM ('MONTHLY', 'ANUAL');

CREATE TABLE subscription_types (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    payment_cycle PaymentCycle NOT NULL,
    price DOUBLE precision NOT NULL,
    currency Currency NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),
    deleted_at TIMESTAMP DEFAULT NULL
);

CREATE TABLE subscriptions (
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
    CONSTRAINT fk_subscription_type_id FOREIGN KEY(subscription_type_id) REFERENCES subscription_types(id),
    CONSTRAINT fk_payments_log_id FOREIGN KEY(payments_log_id) REFERENCES payment_audit_logs(id),
    CONSTRAINT fk_promo_code_id FOREIGN KEY(promo_code_id) REFERENCES promo_codes(id)
);
