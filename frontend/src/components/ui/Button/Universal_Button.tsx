import Link from 'next/link'

interface ButtonProps {
    text: string;
    BtnType?: 'button' | 'submit' | 'reset'; // Restricts input to valid HTML types
    anchor?: string;
    disabled?: boolean;
    className?: string;
};

export const Universal_Button = ({ text = "", BtnType = "button", anchor = '', disabled = false, className = " " }: ButtonProps) => {
    return (
        <div className={className}>
            {anchor ? (
                <Link href={disabled ? anchor : ''} target="_blank" passHref >
                    <p>
                        {text}
                    </p>
                </Link>
            ) : (
                <button type={BtnType} disabled={disabled}>
                    {text}
                </button>
            )}
        </div>
    )
}