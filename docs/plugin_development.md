# Plugin Development Guide

## Overview

The Medical Simulator uses a modular plugin architecture that allows you to easily extend the simulator with new specialties, drugs, scenarios, and physiological models. This guide will walk you through creating your own plugins.

## Plugin Types

### 1. Specialty Plugins
Add new medical specialties with scenarios, procedures, protocols, drugs, lab tests, and imaging studies.

### 2. Drug Plugins
Add comprehensive drug databases with dosing, interactions, and side effects.

### 3. Scenario Plugins
Add new patient scenarios and cases.

### 4. Physiological Plugins
Add new physiological models and organ systems.

## Creating a Specialty Plugin

### Basic Structure

```python
from medsim.core.plugins import SpecialtyPlugin, PluginMetadata

class MySpecialtyPlugin(SpecialtyPlugin):
    def __init__(self):
        metadata = PluginMetadata(
            name="My Specialty",
            version="1.0.0",
            description="Description of your specialty",
            author="Your Name",
            category="specialty",
            tags=["tag1", "tag2"],
            config_schema={
                "option1": {"type": bool},
                "option2": {"type": str}
            }
        )
        
        config = {
            "option1": True,
            "option2": "default_value"
        }
        
        super().__init__(metadata, config)
    
    def _load_specialty_content(self):
        """Load your specialty content here"""
        # Initialize scenarios, procedures, protocols, drugs, etc.
        pass

# Create plugin instance
my_plugin = MySpecialtyPlugin()
```

### Content Types

#### Scenarios
```python
self.scenarios = [
    {
        "id": "unique_scenario_id",
        "title": "Scenario Title",
        "description": "Detailed description",
        "difficulty": "beginner|intermediate|advanced",
        "learning_objectives": [
            "Objective 1",
            "Objective 2"
        ],
        "patient_profile": {
            "age": 45,
            "gender": "male",
            "chief_complaint": "Main complaint",
            "vitals": {
                "blood_pressure_systolic": 120,
                "blood_pressure_diastolic": 80,
                "heart_rate": 80,
                "respiratory_rate": 16,
                "temperature": 37.0,
                "oxygen_saturation": 98
            }
        }
    }
]
```

#### Procedures
```python
self.procedures = [
    {
        "name": "Procedure Name",
        "category": "Category",
        "description": "Detailed description",
        "indications": ["Indication 1", "Indication 2"],
        "contraindications": ["Contraindication 1"],
        "equipment": ["Equipment 1", "Equipment 2"],
        "steps": [
            "Step 1",
            "Step 2"
        ],
        "complications": ["Complication 1"],
        "success_rate": 0.95
    }
]
```

#### Protocols
```python
self.protocols = [
    {
        "name": "Protocol Name",
        "category": "Category",
        "description": "Description",
        "indications": ["Indication 1"],
        "steps": [
            "Step 1",
            "Step 2"
        ],
        "medications": ["Medication 1"],
        "equipment": ["Equipment 1"]
    }
]
```

#### Drugs
```python
self.drugs = [
    {
        "name": "Drug Name",
        "class": "Drug Class",
        "indications": ["Indication 1"],
        "dosing": "Dosing information",
        "contraindications": ["Contraindication 1"],
        "side_effects": ["Side effect 1"]
    }
]
```

#### Lab Tests
```python
self.lab_tests = [
    {
        "name": "Test Name",
        "category": "Category",
        "description": "Description",
        "normal_range": (min, max),
        "critical_value": critical_value,
        "turnaround_time": minutes
    }
]
```

#### Imaging Studies
```python
self.imaging_studies = [
    {
        "name": "Study Name",
        "modality": "Modality",
        "description": "Description",
        "indications": ["Indication 1"],
        "turnaround_time": minutes,
        "cost": cost_in_dollars
    }
]
```

## Plugin Configuration

### Config Schema
Define what configuration options your plugin accepts:

```python
config_schema = {
    "feature_enabled": {"type": bool},
    "max_patients": {"type": int},
    "specialty_name": {"type": str}
}
```

### Configuration Validation
The plugin system automatically validates configuration against your schema.

## Plugin Lifecycle

### Initialization
1. Plugin metadata is validated
2. Configuration is validated against schema
3. `initialize()` is called
4. `_load_specialty_content()` is called

### Cleanup
1. `cleanup()` is called when plugin is unloaded
2. All resources are freed

## Testing Your Plugin

### Manual Testing
1. Place your plugin file in `medsim/plugins/`
2. Start the simulator: `python -m medsim`
3. Use CLI commands to test:
   ```
   medsim> plugins
   medsim> plugin info specialty.myspecialty
   medsim> plugin content specialty.myspecialty scenarios
   ```

### API Testing
```python
from medsim.api import MedicalSimulatorAPI

api = MedicalSimulatorAPI()
response = api.list_plugins()
print(response.data)

response = api.get_plugin_content("specialty.myspecialty", "scenarios")
print(response.data)
```

## Best Practices

### 1. Unique IDs
- Use unique, descriptive IDs for scenarios
- Follow naming convention: `specialty_scenario_##`

### 2. Realistic Data
- Use realistic vital signs, lab values, and clinical data
- Include appropriate normal ranges and critical values

### 3. Comprehensive Content
- Include learning objectives for each scenario
- Provide detailed procedure steps
- List all indications and contraindications

### 4. Documentation
- Document your plugin thoroughly
- Include examples and usage instructions

### 5. Error Handling
- Validate all data in `_load_specialty_content()`
- Handle missing or invalid data gracefully

## Example: Complete Plugin

```python
"""
Example Specialty Plugin
Demonstrates plugin development
"""

from typing import Dict, List, Any
from medsim.core.plugins import SpecialtyPlugin, PluginMetadata

class ExampleSpecialtyPlugin(SpecialtyPlugin):
    def __init__(self):
        metadata = PluginMetadata(
            name="Example Specialty",
            version="1.0.0",
            description="Example specialty for demonstration",
            author="Your Name",
            category="specialty",
            tags=["example", "demo"],
            config_schema={
                "demo_mode": {"type": bool}
            }
        )
        
        config = {"demo_mode": True}
        super().__init__(metadata, config)
    
    def _load_specialty_content(self):
        """Load example content"""
        self.scenarios = [
            {
                "id": "example_scenario_01",
                "title": "Example Patient Case",
                "description": "A patient with example symptoms",
                "difficulty": "intermediate",
                "learning_objectives": [
                    "Learn to diagnose example condition",
                    "Practice example procedure"
                ],
                "patient_profile": {
                    "age": 35,
                    "gender": "female",
                    "chief_complaint": "Example complaint",
                    "vitals": {
                        "blood_pressure_systolic": 120,
                        "blood_pressure_diastolic": 80,
                        "heart_rate": 80,
                        "respiratory_rate": 16,
                        "temperature": 37.0,
                        "oxygen_saturation": 98
                    }
                }
            }
        ]
        
        self.procedures = [
            {
                "name": "Example Procedure",
                "category": "Example",
                "description": "An example procedure",
                "indications": ["Example indication"],
                "contraindications": ["Example contraindication"],
                "equipment": ["Example equipment"],
                "steps": ["Step 1", "Step 2"],
                "complications": ["Example complication"],
                "success_rate": 0.90
            }
        ]

# Plugin instance
example_plugin = ExampleSpecialtyPlugin()
```

## Distribution

### Local Development
Place your plugin in `medsim/plugins/` for development and testing.

### Package Distribution
For distribution, create a Python package:

```
my-medsim-plugin/
├── setup.py
├── README.md
├── my_plugin/
│   ├── __init__.py
│   └── specialty_plugin.py
└── examples/
    └── usage_example.py
```

## Support

For questions or issues with plugin development:
1. Check the existing plugins in `medsim/plugins/`
2. Review the API documentation
3. Test with the provided examples

## Advanced Topics

### Custom Plugin Types
You can create custom plugin types by extending `BasePlugin`:

```python
class CustomPlugin(BasePlugin):
    def initialize(self) -> bool:
        # Your initialization logic
        return True
    
    def cleanup(self) -> None:
        # Your cleanup logic
        pass
```

### Plugin Dependencies
Specify plugin dependencies in metadata:

```python
metadata = PluginMetadata(
    # ... other fields ...
    dependencies=["specialty.cardiology", "drug.antibiotics"]
)
```

### Plugin Events
Plugins can respond to simulation events by implementing event handlers:

```python
def on_patient_update(self, patient_state):
    """Called when patient state changes"""
    pass

def on_medication_administered(self, medication):
    """Called when medication is given"""
    pass
``` 