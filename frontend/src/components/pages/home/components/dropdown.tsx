import InputLabel from "@material-ui/core/InputLabel";
import MenuItem from "@material-ui/core/MenuItem";
import FormControl from "@material-ui/core/FormControl";
import Select from "@material-ui/core/Select";

interface Prop {
    label: string;
    items: string[];
    selected: string;
    onChange: (e: any) => void;
}

const SimpleSelect = ({ label, items, selected, onChange }: Prop) => {
    return (
        <div>
            <FormControl variant="outlined">
                <InputLabel id="label">{label}</InputLabel>
                <Select
                    labelId="selectID"
                    id="demo-simple-select-outlined"
                    value={selected}
                    onChange={onChange}
                    label="Item"
                >
                    <MenuItem value="None">
                        <em>None</em>
                    </MenuItem>
                    {items.map((item) => (
                        <MenuItem value={item}>{item}</MenuItem>
                    ))}
                </Select>
            </FormControl>
        </div>
    );
};
export default SimpleSelect;
