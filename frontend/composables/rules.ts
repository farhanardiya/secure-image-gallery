export const useFormRules = () => {
	return {
		ruleRequired: (v: any) => !!v || "Required",
		ruleUsername: (value: any) => {
			const pattern =
			/^[a-zA-Z0-9_-]{3,20}$/;
			return pattern.test(value) || "Username does not meet requirements";
		},
		rulePassword: (value: any) => {
			const pattern =
			/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{12,50}$/;
			return pattern.test(value) || "Password does not meet requirements";
		},
	};
};
