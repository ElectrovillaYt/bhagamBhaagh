export class AppError extends Error {
    constructor(
        public readonly message: string,
        public readonly statusCode: number = 500,
        public readonly code: string = "INTERNAL_ERROR",
        public readonly cause?: unknown
    ) {
        super(message);
        this.name = "AppError";
    }
};

export class NotFoundError extends AppError {
    constructor(message = "Resource not found") {
        super(message, 404, "NOT_FOUND");
    }
};

export class ValidationError extends AppError {
    constructor(message = "Invalid request") {
        super(message, 400, "VALIDATION_ERROR");
    }
};

export class UnauthorizedError extends AppError {
    constructor(message = "Unauthorized") {
        super(message, 401, "UNAUTHORIZED");
    }
};